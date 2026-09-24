# Density Expand Monitor

time: 2026-07-01T17:18:59
run_group: p1_density_expand_20260701_1655

## Resource
MemFree:        12234576 kB
MemAvailable:   24757976 kB
937, 10940, 0

## Watchdog
[2026-07-01T17:17:55] mem_available_gib=19.67 gpu_free_mib=9692
[2026-07-01T17:18:10] mem_available_gib=21.25 gpu_free_mib=10191
[2026-07-01T17:18:25] mem_available_gib=23.58 gpu_free_mib=10940
[2026-07-01T17:18:40] mem_available_gib=23.62 gpu_free_mib=10940
[2026-07-01T17:18:55] mem_available_gib=23.63 gpu_free_mib=10940

## Progress
done_shards: 18 / 18
raw_csv_files: 18
run_manifests: 18
manager_pid: 163183
PID STAT     ELAPSED CMD

## Done
- [1/1] done label=baseline seed=0 new_rows=120 total_rows=120 elapsed_sec=218.2
- [1/1] done label=baseline seed=1 new_rows=120 total_rows=120 elapsed_sec=226.1
- [1/1] done label=baseline seed=2 new_rows=120 total_rows=120 elapsed_sec=245.3
- [1/1] done label=gated_risk seed=0 new_rows=120 total_rows=120 elapsed_sec=1578.3
- [1/1] done label=gated_risk seed=1 new_rows=120 total_rows=120 elapsed_sec=1689.5
- [1/1] done label=gated_risk seed=2 new_rows=120 total_rows=120 elapsed_sec=1684.1
- [1/1] done label=guard_only seed=0 new_rows=120 total_rows=120 elapsed_sec=1640.6
- [1/1] done label=guard_only seed=1 new_rows=120 total_rows=120 elapsed_sec=1686.1
- [1/1] done label=guard_only seed=2 new_rows=120 total_rows=120 elapsed_sec=1664.0
- [1/1] done label=no_action_guard seed=0 new_rows=120 total_rows=120 elapsed_sec=328.7
- [1/1] done label=no_action_guard seed=1 new_rows=120 total_rows=120 elapsed_sec=219.8
- [1/1] done label=no_action_guard seed=2 new_rows=120 total_rows=120 elapsed_sec=200.7
- [1/1] done label=risk_only seed=0 new_rows=120 total_rows=120 elapsed_sec=1218.2
- [1/1] done label=risk_only seed=1 new_rows=120 total_rows=120 elapsed_sec=1219.4
- [1/1] done label=risk_only seed=2 new_rows=120 total_rows=120 elapsed_sec=1210.2
- [1/1] done label=shield_only seed=0 new_rows=120 total_rows=120 elapsed_sec=1627.9
- [1/1] done label=shield_only seed=1 new_rows=120 total_rows=120 elapsed_sec=1663.9
- [1/1] done label=shield_only seed=2 new_rows=120 total_rows=120 elapsed_sec=1578.8

## Missing
- none

## Exit Codes
- p1_density_expand_20260701_1655_baseline_s0.log: EXIT_CODE=0
- p1_density_expand_20260701_1655_baseline_s1.log: EXIT_CODE=0
- p1_density_expand_20260701_1655_baseline_s2.log: EXIT_CODE=0
- p1_density_expand_20260701_1655_gated_risk_s0.log: EXIT_CODE=0
- p1_density_expand_20260701_1655_gated_risk_s1.log: EXIT_CODE=0
- p1_density_expand_20260701_1655_gated_risk_s2.log: EXIT_CODE=0
- p1_density_expand_20260701_1655_guard_only_s0.log: EXIT_CODE=0
- p1_density_expand_20260701_1655_guard_only_s1.log: EXIT_CODE=0
- p1_density_expand_20260701_1655_guard_only_s2.log: EXIT_CODE=0
- p1_density_expand_20260701_1655_no_action_guard_s0.log: EXIT_CODE=0
- p1_density_expand_20260701_1655_no_action_guard_s1.log: EXIT_CODE=0
- p1_density_expand_20260701_1655_no_action_guard_s2.log: EXIT_CODE=0
- p1_density_expand_20260701_1655_risk_only_s0.log: EXIT_CODE=0
- p1_density_expand_20260701_1655_risk_only_s1.log: EXIT_CODE=0
- p1_density_expand_20260701_1655_risk_only_s2.log: EXIT_CODE=0
- p1_density_expand_20260701_1655_shield_only_s0.log: EXIT_CODE=0
- p1_density_expand_20260701_1655_shield_only_s1.log: EXIT_CODE=0
- p1_density_expand_20260701_1655_shield_only_s2.log: EXIT_CODE=0
