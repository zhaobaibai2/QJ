# Writing Rationale Matrix

| Row ID | Manuscript Unit | Planned Function | Motivation Link | Evidence Anchor | Planned Change | Final Text Check |
|---|---|---|---|---|---|---|
| W0 | Whole paper | Reframe from risk/curriculum to guard/shield-centered safe RL | Current evidence favors action-level safety mechanism | Completion audit + claim boundary matrix | Build Chinese ISCSIC draft around mechanism-separated evidence | No claim says risk-only/full method universally dominates |
| W1 | Abstract | State challenge, method, strongest numbers, boundary | Dense traffic needs progress and safety together | Guard/shield d0.15 and external seeds | Include quantitative comparison and risk-only stagnation caveat | Abstract numbers appear in tables |
| W2 | Introduction | Motivate why reward-only safe RL can fail | Risk-only stagnates, no-action-guard crashes | Table 1 and Table 2 | Present three contributions | Contributions have matching experiments |
| W3 | Method | Explain guard/shield and gated risk exactly enough to reproduce | Method modules must map to code | racrl/config.py and racrl/envs.py | Describe TTC soft/hard braking, speed guard, reward gate | No invented module beyond code |
| W4 | Experiments | Show formal protocol and evidence ladder | ISCSIC needs complete evaluation | n_envs=16 protocol audit | Main, ablation, stress, external seed, parameter sensitivity | No n_envs=8/10/32 in formal claims |
| W5 | Discussion/Conclusion | Preserve claim boundaries and limitations | Avoid overclaiming | Wilson CI overlap and diagnostic tuning decisions | State simulation-only and English-submission boundary | Limitations are explicit |
