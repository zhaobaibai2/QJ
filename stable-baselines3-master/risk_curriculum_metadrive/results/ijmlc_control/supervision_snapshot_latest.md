# IJMLC Supervision Snapshot

time: 2026-07-01T17:24:32
root: /home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive

## GPU
0, NVIDIA GeForce RTX 4070 SUPER, 937, 10940, 0

## Active MetaDrive/Python Jobs
688       1 Ss    1-03:35:02  0.0  0.0 /usr/bin/python3 /usr/bin/networkd-dispatcher --run-startup-triggers
    824       1 Ssl   1-03:35:02  0.0  0.0 /usr/bin/python3 /usr/share/unattended-upgrades/unattended-upgrade-shutdown --wait-for-signal
 166510       1 Ss         29:42  0.0  0.0 /usr/bin/python3 results/ijmlc_control/watchdog_resource_guard.py

## IJMLC Files
raw_csv: 75
summary_tables: 78
run_manifests: 37

## Queue
- P0: control / all / created / next=keep updated
- P1: diagnostic_eval / baseline/risk/guard/shield/gated/no_action / all_core_densities_done / next=generate figures and external baselines
- P1: runtime_overhead / guard/shield/gated/no_action / all_core_densities_done / next=extract Table 7 from all-density aggregate
- P2: external_baseline / PPO-Lagrangian or RCPO / missing / next=inspect SB3/contrib availability then implement simplest stable baseline
- P2: external_baseline / RSS/TTC classical filter / missing / next=implement/evaluate frozen policy with classical filter
- P3: seed_extension / core methods seed3 seed4 / pending / next=train if diagnostic gap remains after frozen eval
- P4: density_sweep / core methods d0.00-0.25 / done / next=use p1_all_density_core_aggregate.csv for Fig5/Table6
- P5: sensitivity / thresholds and target speed / pending / next=frozen-model sensitivity first
- P6: writing / Springer manuscript / pending / next=after stable summaries
