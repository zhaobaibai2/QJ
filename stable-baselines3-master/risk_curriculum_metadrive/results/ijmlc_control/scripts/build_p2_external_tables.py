#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from datetime import datetime
import json
import pandas as pd
import numpy as np

ROOT=Path('/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive')
CTL=ROOT/'results/ijmlc_control'
RAW_DIR=CTL/'raw_csv'
SUMMARY_DIR=CTL/'summary_tables'
MANUSCRIPT=CTL/'manuscript'
P2=CTL/'p2_external_baselines'
RUN_GROUP='ijmlc_p2_external_20260701_1733'
MANUSCRIPT.mkdir(parents=True, exist_ok=True)
SUMMARY_DIR.mkdir(parents=True, exist_ok=True)

METHOD_LABELS={
    'baseline':'PPO',
    'rss_ttc_filter':'RSS/TTC filter',
    'rcpo_lagrangian':'RCPO-Lagrangian',
    'guard_only':'Guard',
    'shield_only':'Shield',
    'gated_risk':'Gated-risk',
}
ORDER=['baseline','rss_ttc_filter','rcpo_lagrangian','guard_only','shield_only','gated_risk']
METRICS=['success','cost','route_completion','collision','out_of_road','mean_speed_kmh','median_speed_kmh','stop_ratio','low_progress','ttc_dangerous_fraction','intervention_rate_per_100_steps','intervention_rate_per_km','policy_inference_ms_mean','policy_inference_ms_p95','control_loop_wall_ms_mean','control_loop_wall_ms_p95']

def load_existing_core():
    p=RAW_DIR/'p1_all_density_core_episodes.csv'
    if not p.exists():
        return pd.DataFrame()
    df=pd.read_csv(p)
    return df[df['label'].isin(['baseline','guard_only','shield_only','gated_risk'])].copy()

def load_p2_raw():
    files=[]
    for seed in [0,1,2]:
        files.append(RAW_DIR/f'{RUN_GROUP}_rss_ttc_s{seed}_episodes.csv')
        files.append(RAW_DIR/f'{RUN_GROUP}_rcpo_diag_s{seed}_episodes.csv')
    present=[p for p in files if p.exists()]
    frames=[]
    for p in present:
        df=pd.read_csv(p)
        df['source_file']=str(p)
        frames.append(df)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(), files, present

def summarize(df):
    if df.empty:
        return pd.DataFrame()
    rows=[]
    for (label,density), g in df.groupby(['label','density'], dropna=False):
        row={'label':label,'method':METHOD_LABELS.get(label,label),'density':density,'episodes':len(g),'train_seeds':g['train_seed'].nunique() if 'train_seed' in g else np.nan}
        for m in METRICS:
            if m in g:
                row[m]=float(g[m].mean())
        rows.append(row)
    out=pd.DataFrame(rows)
    if out.empty:
        return out
    out['order']=out['label'].map(lambda x: ORDER.index(x) if x in ORDER else len(ORDER))
    return out.sort_values(['density','order']).drop(columns=['order'])

def pct(s):
    return s*100.0

def main():
    p2_raw, expected, present = load_p2_raw()
    core = load_existing_core()
    combined = pd.concat([core, p2_raw], ignore_index=True) if not core.empty or not p2_raw.empty else pd.DataFrame()
    report=[]
    report.append('# P2 External Baseline Table Build\n\n')
    report.append(f'generated_at: {datetime.now().isoformat(timespec="seconds")}\n')
    report.append(f'present_p2_files: {len(present)} / {len(expected)}\n')
    missing=[str(p) for p in expected if not p.exists()]
    if missing:
        report.append('\n## Missing\n')
        for p in missing:
            report.append(f'- `{p}`\n')
    if not p2_raw.empty:
        p=RAW_DIR/'p2_external_all_episodes.csv'
        p2_raw.to_csv(p,index=False)
        report.append(f'\nraw_p2: `{p}` rows={len(p2_raw)}\n')
    if not combined.empty:
        agg=summarize(combined)
        p=SUMMARY_DIR/'p2_external_with_core_aggregate.csv'
        agg.round(6).to_csv(p,index=False)
        report.append(f'aggregate: `{p}` rows={len(agg)}\n')
        d015=agg[np.isclose(agg['density'],0.15)].copy()
        table=pd.DataFrame({
            'method':d015['method'],
            'episodes':d015['episodes'],
            'train_seeds':d015['train_seeds'],
            'success_pct':pct(d015['success']),
            'cost_pct':pct(d015['cost']),
            'route_completion_pct':pct(d015['route_completion']),
            'collision_pct':pct(d015['collision']),
            'out_of_road_pct':pct(d015['out_of_road']),
            'low_progress_pct':pct(d015['low_progress']),
            'stop_ratio_pct':pct(d015['stop_ratio']),
            'mean_speed_kmh':d015['mean_speed_kmh'],
            'ttc_dangerous_pct':pct(d015['ttc_dangerous_fraction']),
            'interventions_per_100_steps':d015['intervention_rate_per_100_steps'],
            'control_loop_p95_ms':d015['control_loop_wall_ms_p95'],
        }).round(3)
        p=MANUSCRIPT/'table4_external_baselines_d015.csv'
        table.to_csv(p,index=False)
        report.append(f'table4_csv: `{p}` rows={len(table)}\n')
        ptex=MANUSCRIPT/'table4_external_baselines_d015.tex'
        table.to_latex(ptex,index=False,escape=True,float_format='%.3f')
        report.append(f'table4_tex: `{ptex}`\n')
    else:
        report.append('\nNo data available yet.\n')
    out=CTL/'P2_EXTERNAL_BASELINES_TABLE_REPORT.md'
    out.write_text(''.join(report), encoding='utf-8')
    print(out)

if __name__=='__main__':
    main()
