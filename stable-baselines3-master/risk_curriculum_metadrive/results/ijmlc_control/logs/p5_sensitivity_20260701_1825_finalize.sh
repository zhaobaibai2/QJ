#!/usr/bin/env bash
set -u
cd /home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive
RUN_GROUP=p5_sensitivity_20260701_1825
PID_FILE=results/ijmlc_control/logs/${RUN_GROUP}_manager.pid
STATUS=results/ijmlc_control/p5_sensitivity_finalize_status.txt
echo "started $(date --iso-8601=seconds)" > "$STATUS"
while true; do
  if [ -f "$PID_FILE" ]; then
    pid=$(cat "$PID_FILE" 2>/dev/null || true)
    if [ -n "$pid" ] && ps -p "$pid" >/dev/null 2>&1; then sleep 60; continue; fi
  fi
  break
done
/home/aaa/miniconda3/envs/sb3/bin/python - <<'PYFINAL'
from pathlib import Path
from datetime import datetime
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path('/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive')
CTL=ROOT/'results/ijmlc_control'
RUN='p5_sensitivity_20260701_1825'
raw_files=sorted((CTL/'raw_csv').glob(f'{RUN}_*_episodes.csv'))
frames=[]
for p in raw_files:
    df=pd.read_csv(p); df['source_file']=str(p); frames.append(df)
if not frames:
    raise SystemExit('no sensitivity raw files')
raw=pd.concat(frames, ignore_index=True)
raw_out=CTL/'raw_csv/p5_sensitivity_all_episodes.csv'
raw.to_csv(raw_out,index=False)
metrics=['success','cost','route_completion','collision','out_of_road','mean_speed_kmh','stop_ratio','low_progress','ttc_dangerous_fraction','intervention_rate_per_100_steps','control_loop_wall_ms_p95']
agg=raw.groupby(['label','sensitivity_axis','sensitivity_value'], dropna=False).agg(episodes=('episode','count'), train_seeds=('train_seed','nunique'), **{m:(m,'mean') for m in metrics}).reset_index()
agg['sensitivity_value_num']=pd.to_numeric(agg['sensitivity_value'], errors='coerce')
order={'guard_only':0,'shield_only':1,'gated_risk':2}
agg['order']=agg['label'].map(order)
agg=agg.sort_values(['sensitivity_axis','order','sensitivity_value_num']).drop(columns=['order'])
summary_out=CTL/'summary_tables/p5_sensitivity_aggregate.csv'
agg.round(6).to_csv(summary_out,index=False)
method_map={'guard_only':'Guard','shield_only':'Shield','gated_risk':'Gated-risk'}
table=agg.copy()
table['method']=table['label'].map(method_map)
for c in ['success','cost','route_completion','low_progress','stop_ratio','ttc_dangerous_fraction']:
    table[c+'_pct']=table[c]*100
cols=['sensitivity_axis','sensitivity_value','method','episodes','train_seeds','success_pct','cost_pct','route_completion_pct','low_progress_pct','stop_ratio_pct','ttc_dangerous_fraction_pct','intervention_rate_per_100_steps','control_loop_wall_ms_p95']
table=table[cols].round(3)
man=CTL/'manuscript/table_supp_sensitivity.csv'
table.to_csv(man,index=False)
# figures
fig_dir=CTL/'figures'; fig_dir.mkdir(exist_ok=True)
colors={'guard_only':'#54A24B','shield_only':'#72B7B2','gated_risk':'#E45756'}
for axis, pretty in [('ttc_threshold','TTC threshold'),('target_speed_kmh','Target speed (km/h)')]:
    sub=agg[agg['sensitivity_axis'].eq(axis)].copy()
    fig, axes=plt.subplots(1,3,figsize=(11.5,3.6),sharex=True)
    for label in ['guard_only','shield_only','gated_risk']:
        s=sub[sub['label'].eq(label)].sort_values('sensitivity_value_num')
        if s.empty: continue
        name=method_map[label]
        axes[0].plot(s['sensitivity_value_num'],s['success']*100,marker='o',label=name,color=colors[label])
        axes[1].plot(s['sensitivity_value_num'],s['cost']*100,marker='o',label=name,color=colors[label])
        axes[2].plot(s['sensitivity_value_num'],s['route_completion']*100,marker='o',label=name,color=colors[label])
    for ax,y in zip(axes,['Success (%)','Cost (%)','Route completion (%)']):
        ax.set_xlabel(pretty); ax.set_ylabel(y); ax.grid(True,color='#E5E5E5'); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    axes[0].legend(frameon=False,fontsize=8)
    fig.suptitle(f'Sensitivity at density 0.15: {pretty}',fontsize=12)
    fig.tight_layout(rect=(0,0,1,0.93))
    for ext in ['pdf','png']:
        fig.savefig(fig_dir/f'fig7_sensitivity_{axis}.{ext}',dpi=300,bbox_inches='tight')
    plt.close(fig)
report=CTL/'P5_SENSITIVITY_REPORT.md'
lines=['# P5 Sensitivity Report\n\n',f'generated_at: {datetime.now().isoformat(timespec="seconds")}\n',f'raw_files: {len(raw_files)}\n',f'raw_rows: {len(raw)}\n',f'raw_csv: `{raw_out}`\n',f'aggregate_csv: `{summary_out}`\n',f'table_csv: `{man}`\n','figures: `fig7_sensitivity_ttc_threshold.*`, `fig7_sensitivity_target_speed_kmh.*`\n']
report.write_text(''.join(lines),encoding='utf-8')
print(report)
PYFINAL
code=$?
echo "finished $(date --iso-8601=seconds) exit=$code" >> "$STATUS"
exit $code
