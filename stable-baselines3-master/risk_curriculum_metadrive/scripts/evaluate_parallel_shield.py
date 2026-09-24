#!/usr/bin/env python
from __future__ import annotations
import argparse, math, sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
import pandas as pd
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

def run_one(args_tuple):
    model_name, model_path, mode, density, episode, horizon = args_tuple
    import math, sys
    from pathlib import Path
    sys.path.insert(0, str(Path.cwd()))
    from stable_baselines3 import PPO
    from metadrive.examples import expert
    from racrl.config import get_variant_config
    from racrl.envs import build_env
    config = get_variant_config('proposed', 'ppo', seed=0, timesteps=0)
    config.horizon = horizon
    env = build_env(config, training=False, density=density)
    model = None
    if mode in {'rl', 'shield_expert'}:
        model = PPO.load(str(model_path), device='cpu')
    try:
        obs, _ = env.reset(seed=config.test_start_seed + episode)
        done = False
        final = {}
        steps = 0
        takeover = 0
        while not done:
            if mode == 'expert':
                action = expert(env.env.env.agent, deterministic=True)
                takeover += 1
            else:
                action, _ = model.predict(obs, deterministic=True)
                if mode == 'shield_expert':
                    _, min_ttc = env.env._ttc_risk()
                    lane = env.env._lane_deviation()
                    speed = float(env.env.env.agent.speed_km_h)
                    if (math.isfinite(min_ttc) and min_ttc < 8.0) or lane > 0.75 or speed > 25.0:
                        action = expert(env.env.env.agent, deterministic=True)
                        takeover += 1
            obs, reward, terminated, truncated, info = env.step(action)
            done = bool(terminated or truncated)
            steps += 1
            if done:
                final = info
        return {
            'model': model_name, 'mode': mode, 'density': density, 'episode': episode,
            'success': final.get('is_success', 0.0),
            'route_completion': final.get('episode_route_completion', float('nan')),
            'collision': final.get('episode_collision', 0.0),
            'out_of_road': final.get('episode_out_of_road', 0.0),
            'cost': final.get('episode_cost', 0.0),
            'reward': final.get('episode_base_reward', float('nan')),
            'shaped_reward': final.get('episode_shaped_reward', float('nan')),
            'episode_length': final.get('episode_length', steps),
            'mean_speed_kmh': final.get('episode_mean_speed', float('nan')),
            'mean_lane_deviation': final.get('episode_mean_lane_deviation', float('nan')),
            'steering_variation': final.get('episode_steering_variation', float('nan')),
            'ttc_risk': final.get('episode_ttc_risk', float('nan')),
            'min_ttc': final.get('episode_min_ttc', float('nan')),
            'takeover_rate': takeover / max(steps, 1),
        }
    finally:
        env.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--episodes', type=int, default=50)
    parser.add_argument('--workers', type=int, default=24)
    parser.add_argument('--horizon', type=int, default=1200)
    parser.add_argument('--output-dir', type=Path, default=Path('outputs/policy_shield_screen/evaluations'))
    args = parser.parse_args()
    models = {
        'expert_only': None,
        'rl_s0_100w': Path('outputs/stage1000_true_proposed_s0/runs/proposed_ppo_s0/model/final_model.zip'),
        'rl_s1_100w': Path('outputs/stage1000_true_proposed_multiseed/runs/proposed_ppo_s1/model/final_model.zip'),
        'rl_ckpt702': Path('outputs/stage1000_final_candidate/runs/proposed_ppo_s0/model/final_model.zip'),
    }
    jobs = []
    for model_name, model_path in models.items():
        modes = ['expert'] if model_name == 'expert_only' else ['rl', 'shield_expert']
        if model_path is not None and not model_path.exists():
            continue
        for mode in modes:
            for density in (0.00, 0.08, 0.15):
                for episode in range(args.episodes):
                    jobs.append((model_name, model_path, mode, density, episode, args.horizon))
    rows = []
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run_one, job) for job in jobs]
        for i, fut in enumerate(as_completed(futures), 1):
            row = fut.result()
            rows.append(row)
            if i % 20 == 0 or i == len(jobs):
                print(f'completed {i}/{len(jobs)} latest={row}', flush=True)
                pd.DataFrame(rows).to_csv(args.output_dir / 'shield_screen_partial.csv', index=False)
    df = pd.DataFrame(rows)
    out = args.output_dir / 'shield_screen.csv'
    df.to_csv(out, index=False)
    summary = df.groupby(['model','mode','density'], as_index=False).agg(
        success=('success','mean'), route_completion=('route_completion','mean'), collision=('collision','mean'),
        out_of_road=('out_of_road','mean'), cost=('cost','mean'), reward=('reward','mean'), takeover_rate=('takeover_rate','mean')
    )
    summary.to_csv(args.output_dir / 'summary.csv', index=False)
    print(summary.to_string(index=False), flush=True)
    print(f'saved={out}', flush=True)
if __name__ == '__main__':
    main()
