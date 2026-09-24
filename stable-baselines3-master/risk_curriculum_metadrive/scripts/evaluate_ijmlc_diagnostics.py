#!/usr/bin/env python3
"""Evaluate frozen models for IJMLC-specific diagnostics.

The old paper tables already contain success, cost, route completion, collision,
and intervention rates. This script adds journal-reviewer diagnostics that were
not fully present in the old CSVs: stop ratio, median speed, low-progress rate,
TTC danger fraction, intervention per km, and wall-clock action latency.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import replace
import math
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from stable_baselines3 import PPO, SAC

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'scripts'))

from evaluate_from_config import load_config  # noqa: E402
from racrl.bootstrap import resolve_device  # noqa: E402
from racrl.envs import build_env  # noqa: E402


def finite_array(values: list[float]) -> np.ndarray:
    arr = np.asarray(values, dtype=float)
    return arr[np.isfinite(arr)]


def mean(values: list[float]) -> float:
    arr = finite_array(values)
    return float(arr.mean()) if arr.size else float('nan')


def pct(values: list[float], q: float) -> float:
    arr = finite_array(values)
    return float(np.percentile(arr, q)) if arr.size else float('nan')


def load_manifest(path: Path, labels: set[str] | None, seeds: set[int] | None) -> list[dict[str, str]]:
    with path.open(newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    selected = []
    for row in rows:
        if labels and row.get('label') not in labels:
            continue
        if seeds and int(row.get('seed', -9999)) not in seeds:
            continue
        if row.get('config_exists') != 'True' or row.get('model_exists') != 'True':
            continue
        selected.append(row)
    return selected


def episode_row(
    *,
    manifest_row: dict[str, str],
    density: float,
    start_seed: int,
    episode: int,
    map_seed: int,
    final_info: dict[str, Any],
    shaped_reward: float,
    speeds: list[float],
    ttcs: list[float],
    ttc_risks: list[float],
    policy_ms: list[float],
    env_step_ms: list[float],
    control_ms: list[float],
    path_length_m: float,
    danger_ttc: float,
    action_filter: str = 'none',
    sensitivity_axis: str = '',
    sensitivity_value: str = '',
    override_ttc_threshold: float | None = None,
    override_target_speed_kmh: float | None = None,
) -> dict[str, Any]:
    steps = max(len(speeds), 1)
    speed_arr = finite_array(speeds)
    ttc_arr = finite_array(ttcs)
    success = float(final_info.get('is_success', 0.0) or 0.0)
    cost = float(final_info.get('episode_cost', 0.0) or 0.0)
    route = float(final_info.get('episode_route_completion', np.nan))
    intervention = float(final_info.get('shield_intervention', 0.0) or 0.0)
    stop_ratio = float(np.mean(speed_arr < 1.0)) if speed_arr.size else float('nan')
    low_progress = float(route < 0.2) if np.isfinite(route) else float('nan')
    distance_km = max(path_length_m / 1000.0, 1e-9)
    return {
        'label': manifest_row['label'],
        'role': manifest_row.get('role', ''),
        'variant': manifest_row['variant'],
        'algo': manifest_row['algo'],
        'train_seed': int(manifest_row['seed']),
        'action_filter': action_filter,
        'sensitivity_axis': sensitivity_axis,
        'sensitivity_value': sensitivity_value,
        'override_ttc_threshold': override_ttc_threshold,
        'override_target_speed_kmh': override_target_speed_kmh,
        'density': density,
        'scenario_start_seed': start_seed,
        'map_seed': map_seed,
        'episode': episode,
        'success': success,
        'cost': cost,
        'route_completion': route,
        'collision': float(final_info.get('episode_collision', 0.0) or 0.0),
        'crash_vehicle': float(final_info.get('episode_crash_vehicle', 0.0) or 0.0),
        'crash_object': float(final_info.get('episode_crash_object', 0.0) or 0.0),
        'out_of_road': float(final_info.get('episode_out_of_road', 0.0) or 0.0),
        'episode_length': float(final_info.get('episode_length', steps) or steps),
        'reward': float(final_info.get('episode_base_reward', np.nan)),
        'shaped_reward': shaped_reward,
        'mean_speed_kmh': mean(speeds),
        'median_speed_kmh': pct(speeds, 50),
        'p10_speed_kmh': pct(speeds, 10),
        'stop_ratio': stop_ratio,
        'low_progress': low_progress,
        'progress_per_cost': route / max(cost, 1e-6) if np.isfinite(route) else float('nan'),
        'path_length_m': path_length_m,
        'mean_ttc': mean(ttcs),
        'min_ttc': float(ttc_arr.min()) if ttc_arr.size else float('nan'),
        'ttc_risk_mean': mean(ttc_risks),
        'ttc_dangerous_fraction': float(np.mean(ttc_arr < danger_ttc)) if ttc_arr.size else 0.0,
        'intervention_count': intervention,
        'soft_guard_count': float(final_info.get('shield_soft', 0.0) or 0.0),
        'hard_shield_count': float(final_info.get('shield_hard', 0.0) or 0.0),
        'overspeed_guard_count': float(final_info.get('overspeed_guard', 0.0) or 0.0),
        'intervention_rate_per_100_steps': intervention / steps * 100.0,
        'intervention_rate_per_km': intervention / distance_km,
        'policy_inference_ms_mean': mean(policy_ms),
        'policy_inference_ms_p50': pct(policy_ms, 50),
        'policy_inference_ms_p95': pct(policy_ms, 95),
        'policy_inference_ms_p99': pct(policy_ms, 99),
        'env_step_wall_ms_mean': mean(env_step_ms),
        'env_step_wall_ms_p95': pct(env_step_ms, 95),
        'control_loop_wall_ms_mean': mean(control_ms),
        'control_loop_wall_ms_p95': pct(control_ms, 95),
        'total_action_latency_ms_mean': mean(policy_ms),
        'total_action_latency_ms_p95': pct(policy_ms, 95),
        'source_config_json': manifest_row['config_json'],
        'source_model_path': manifest_row['model'],
    }


def apply_action_filter(env, action, args: argparse.Namespace) -> tuple[np.ndarray, int, int, int, int]:
    """Apply an external runtime braking filter to a model action.

    This is intentionally outside RiskAwareMetaDriveWrapper so it can be treated
    as a same-checkpoint runtime operator, not a retrained policy.
    """
    action_arr = np.asarray(action, dtype=np.float32).copy()
    if args.action_filter == 'none' or action_arr.shape[0] < 2:
        return action_arr, 0, 0, 0, 0
    supported_filters = {'rss_ttc', 'runtime_ttc', 'runtime_speed', 'runtime_ttc_speed'}
    if args.action_filter not in supported_filters:
        raise ValueError(f'Unsupported action_filter={args.action_filter!r}')
    wrapper = getattr(env, 'env', env)
    intervention = soft = hard = overspeed = 0
    try:
        _, min_ttc = wrapper._ttc_risk()
    except Exception:
        min_ttc = math.inf
    try:
        speed_kmh = float(wrapper.env.agent.speed_km_h)
    except Exception:
        speed_kmh = float('nan')
    before = float(action_arr[1])
    if args.action_filter == 'rss_ttc':
        apply_ttc = True
        apply_speed = True
        hard_ttc = float(args.rss_hard_ttc)
        soft_ttc = float(args.rss_soft_ttc)
        target_speed = float(args.rss_target_speed_kmh)
    else:
        apply_ttc = args.action_filter in {'runtime_ttc', 'runtime_ttc_speed'}
        apply_speed = args.action_filter in {'runtime_speed', 'runtime_ttc_speed'}
        hard_ttc = float(args.runtime_hard_ttc)
        soft_ttc = float(args.runtime_ttc_threshold)
        target_speed = float(args.runtime_target_speed_kmh)
    if apply_ttc:
        if math.isfinite(min_ttc) and min_ttc < hard_ttc:
            action_arr[1] = min(float(action_arr[1]), -1.0)
            hard = int(float(action_arr[1]) != before)
        elif math.isfinite(min_ttc) and min_ttc < soft_ttc:
            action_arr[1] = min(float(action_arr[1]), -0.6)
            soft = int(float(action_arr[1]) != before)
    if apply_speed:
        if math.isfinite(speed_kmh) and speed_kmh > target_speed + 5.0:
            prev = float(action_arr[1])
            action_arr[1] = min(float(action_arr[1]), -0.35)
            overspeed = int(float(action_arr[1]) != prev)
        elif math.isfinite(speed_kmh) and speed_kmh > target_speed:
            prev = float(action_arr[1])
            action_arr[1] = min(float(action_arr[1]), 0.0)
            overspeed = int(float(action_arr[1]) != prev)
    intervention = int(bool(soft or hard or overspeed))
    return action_arr, intervention, soft, hard, overspeed


def summarize(frame: pd.DataFrame) -> pd.DataFrame:
    if frame.empty:
        return frame
    metrics = [
        'success', 'cost', 'route_completion', 'collision', 'out_of_road',
        'mean_speed_kmh', 'median_speed_kmh', 'stop_ratio', 'low_progress',
        'progress_per_cost', 'mean_ttc', 'min_ttc', 'ttc_dangerous_fraction',
        'intervention_rate_per_100_steps', 'intervention_rate_per_km',
        'policy_inference_ms_mean', 'policy_inference_ms_p95',
        'env_step_wall_ms_mean', 'env_step_wall_ms_p95',
        'control_loop_wall_ms_mean', 'control_loop_wall_ms_p95',
    ]
    grouped = frame.groupby(['label', 'density'], dropna=False)
    rows = []
    for (label, density), group in grouped:
        row = {'label': label, 'density': density, 'episodes': len(group), 'train_seeds': group['train_seed'].nunique()}
        for metric in metrics:
            row[f'{metric}_mean'] = float(group[metric].mean())
            row[f'{metric}_std'] = float(group[metric].std(ddof=1)) if len(group) > 1 else 0.0
        rows.append(row)
    return pd.DataFrame(rows).sort_values(['density', 'label'])


def evaluate_one(row: dict[str, str], args: argparse.Namespace) -> list[dict[str, Any]]:
    config = load_config(Path(row['config_json']))
    reward_updates = {}
    if args.override_ttc_threshold is not None:
        reward_updates['ttc_threshold'] = float(args.override_ttc_threshold)
    if args.override_target_speed_kmh is not None:
        reward_updates['target_speed_kmh'] = float(args.override_target_speed_kmh)
    if reward_updates:
        config.reward_weights = replace(config.reward_weights, **reward_updates)
    config.test_scenarios = max(int(config.test_scenarios), max(args.episodes_per_start + 1, 20))
    config.n_envs = 1
    algorithm = PPO if config.algo == 'ppo' else SAC
    out_rows: list[dict[str, Any]] = []
    for density in args.densities:
        for start_seed in args.test_start_seeds:
            config.test_start_seed = int(start_seed)
            env = build_env(config, output_file=None, training=False, density=float(density))
            model = algorithm.load(row['model'], env=env, device=args.device)
            try:
                for episode in range(args.episodes_per_start):
                    map_seed = int(start_seed) + episode
                    obs, _ = env.reset(seed=map_seed)
                    done = False
                    shaped_reward = 0.0
                    speeds: list[float] = []
                    ttcs: list[float] = []
                    ttc_risks: list[float] = []
                    policy_ms: list[float] = []
                    env_step_ms: list[float] = []
                    control_ms: list[float] = []
                    path_length_m = 0.0
                    prev_xy: tuple[float, float] | None = None
                    final_info: dict[str, Any] = {}
                    external_interventions = 0
                    external_soft = 0
                    external_hard = 0
                    external_overspeed = 0
                    while not done:
                        t0 = time.perf_counter()
                        action, _ = model.predict(obs, deterministic=True)
                        action, ext_i, ext_soft, ext_hard, ext_over = apply_action_filter(env, action, args)
                        external_interventions += ext_i
                        external_soft += ext_soft
                        external_hard += ext_hard
                        external_overspeed += ext_over
                        p_ms = (time.perf_counter() - t0) * 1000.0
                        t1 = time.perf_counter()
                        obs, reward, terminated, truncated, info = env.step(action)
                        e_ms = (time.perf_counter() - t1) * 1000.0
                        policy_ms.append(p_ms)
                        env_step_ms.append(e_ms)
                        control_ms.append(p_ms + e_ms)
                        shaped_reward += float(reward)
                        speeds.append(float(info.get('vehicle_speed_kmh', np.nan)))
                        ttcs.append(float(info.get('min_ttc', np.nan)))
                        ttc_risks.append(float(info.get('ttc_risk', np.nan)))
                        x = float(info.get('vehicle_x', np.nan))
                        y = float(info.get('vehicle_y', np.nan))
                        if np.isfinite(x) and np.isfinite(y):
                            if prev_xy is not None:
                                path_length_m += math.hypot(x - prev_xy[0], y - prev_xy[1])
                            prev_xy = (x, y)
                        done = bool(terminated or truncated)
                        if done:
                            final_info = dict(info)
                    if args.action_filter != 'none':
                        final_info['shield_intervention'] = float(final_info.get('shield_intervention', 0.0) or 0.0) + float(external_interventions)
                        final_info['shield_soft'] = float(final_info.get('shield_soft', 0.0) or 0.0) + float(external_soft)
                        final_info['shield_hard'] = float(final_info.get('shield_hard', 0.0) or 0.0) + float(external_hard)
                        final_info['overspeed_guard'] = float(final_info.get('overspeed_guard', 0.0) or 0.0) + float(external_overspeed)
                    out_rows.append(episode_row(
                        manifest_row=row,
                        density=float(density),
                        start_seed=int(start_seed),
                        episode=episode,
                        map_seed=map_seed,
                        final_info=final_info,
                        shaped_reward=shaped_reward,
                        speeds=speeds,
                        ttcs=ttcs,
                        ttc_risks=ttc_risks,
                        policy_ms=policy_ms,
                        env_step_ms=env_step_ms,
                        control_ms=control_ms,
                        path_length_m=path_length_m,
                        danger_ttc=float(args.danger_ttc_threshold),
                        action_filter=str(args.action_filter),
                        sensitivity_axis=str(args.sensitivity_axis or ''),
                        sensitivity_value=str(args.sensitivity_value or ''),
                        override_ttc_threshold=args.override_ttc_threshold,
                        override_target_speed_kmh=args.override_target_speed_kmh,
                    ))
            finally:
                env.close()
    return out_rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--manifest', type=Path, default=ROOT / 'results' / 'ijmlc_control' / '06_EXISTING_MODEL_MANIFEST.csv')
    parser.add_argument('--labels', nargs='+', default=['baseline', 'risk_only', 'guard_only', 'shield_only', 'gated_risk', 'no_action_guard'])
    parser.add_argument('--seeds', type=int, nargs='*', default=None)
    parser.add_argument('--densities', type=float, nargs='+', default=[0.15])
    parser.add_argument('--test-start-seeds', type=int, nargs='+', default=[10000])
    parser.add_argument('--episodes-per-start', type=int, default=20)
    parser.add_argument('--device', default='cuda')
    parser.add_argument('--danger-ttc-threshold', type=float, default=5.0)
    parser.add_argument(
        '--action-filter',
        choices=['none', 'rss_ttc', 'runtime_ttc', 'runtime_speed', 'runtime_ttc_speed'],
        default='none',
    )
    parser.add_argument('--rss-soft-ttc', type=float, default=6.0)
    parser.add_argument('--rss-hard-ttc', type=float, default=3.5)
    parser.add_argument('--rss-target-speed-kmh', type=float, default=20.0)
    parser.add_argument('--runtime-ttc-threshold', type=float, default=12.0)
    parser.add_argument('--runtime-hard-ttc', type=float, default=7.2)
    parser.add_argument('--runtime-target-speed-kmh', type=float, default=18.0)
    parser.add_argument('--override-ttc-threshold', type=float, default=None)
    parser.add_argument('--override-target-speed-kmh', type=float, default=None)
    parser.add_argument('--sensitivity-axis', default='')
    parser.add_argument('--sensitivity-value', default='')
    parser.add_argument('--run-id', default=None)
    parser.add_argument('--max-models', type=int, default=None)
    args = parser.parse_args()

    resolve_device(args.device)
    labels = set(args.labels) if args.labels else None
    seeds = set(args.seeds) if args.seeds else None
    rows = load_manifest(args.manifest, labels, seeds)
    if args.max_models is not None:
        rows = rows[:args.max_models]
    if not rows:
        raise SystemExit('No manifest rows selected')

    run_id = args.run_id or 'ijmlc_diag_' + datetime.now().strftime('%Y%m%d_%H%M%S')
    out_root = ROOT / 'results' / 'ijmlc_control'
    raw_dir = out_root / 'raw_csv'
    summary_dir = out_root / 'summary_tables'
    manifest_dir = out_root / 'run_manifests'
    log_dir = out_root / 'logs'
    for d in [raw_dir, summary_dir, manifest_dir, log_dir]:
        d.mkdir(parents=True, exist_ok=True)

    all_rows: list[dict[str, Any]] = []
    start_wall = time.time()
    partial_episode_path = raw_dir / f'{run_id}_episodes.partial.csv'
    partial_summary_path = summary_dir / f'{run_id}_summary.partial.csv'
    for i, row in enumerate(rows, start=1):
        model_start = time.time()
        print(f'[{i}/{len(rows)}] start label={row["label"]} seed={row["seed"]}', flush=True)
        new_rows = evaluate_one(row, args)
        all_rows.extend(new_rows)
        partial_episodes = pd.DataFrame(all_rows)
        partial_episodes.to_csv(partial_episode_path, index=False)
        summarize(partial_episodes).to_csv(partial_summary_path, index=False)
        print(
            f'[{i}/{len(rows)}] done label={row["label"]} seed={row["seed"]} '
            f'new_rows={len(new_rows)} total_rows={len(all_rows)} elapsed_sec={time.time() - model_start:.1f}',
            flush=True,
        )

    episodes = pd.DataFrame(all_rows)
    summary = summarize(episodes)
    episode_path = raw_dir / f'{run_id}_episodes.csv'
    summary_path = summary_dir / f'{run_id}_summary.csv'
    episodes.to_csv(episode_path, index=False)
    summary.to_csv(summary_path, index=False)
    run_manifest = {
        'run_id': run_id,
        'created_at': datetime.now().isoformat(timespec='seconds'),
        'manifest': str(args.manifest),
        'labels': args.labels,
        'seeds': args.seeds,
        'densities': args.densities,
        'test_start_seeds': args.test_start_seeds,
        'episodes_per_start': args.episodes_per_start,
        'selected_models': len(rows),
        'episode_rows': len(episodes),
        'action_filter': args.action_filter,
        'rss_soft_ttc': args.rss_soft_ttc,
        'rss_hard_ttc': args.rss_hard_ttc,
        'rss_target_speed_kmh': args.rss_target_speed_kmh,
        'runtime_ttc_threshold': args.runtime_ttc_threshold,
        'runtime_hard_ttc': args.runtime_hard_ttc,
        'runtime_target_speed_kmh': args.runtime_target_speed_kmh,
        'override_ttc_threshold': args.override_ttc_threshold,
        'override_target_speed_kmh': args.override_target_speed_kmh,
        'sensitivity_axis': args.sensitivity_axis,
        'sensitivity_value': args.sensitivity_value,
        'episode_csv': str(episode_path),
        'summary_csv': str(summary_path),
        'elapsed_sec': time.time() - start_wall,
        'status': 'done',
        'claim_supported': 'IJMLC non-motion artifact, progress-safety frontier, runtime wall-clock diagnostics',
        'boundary_note': 'Frozen-model diagnostic evaluation; not new training or retuning evidence.',
    }
    manifest_path = manifest_dir / f'{run_id}.json'
    manifest_path.write_text(json.dumps(run_manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(run_manifest, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
