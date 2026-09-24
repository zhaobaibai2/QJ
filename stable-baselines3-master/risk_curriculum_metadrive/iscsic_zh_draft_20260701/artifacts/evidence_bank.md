# Evidence Bank

## Main claim

在 MetaDrive 密集交通设置中，动作级安全守护/屏蔽是稳定安全驾驶的主机制；风险奖励、TTC、车道和平滑项以及门控风险塑形是围绕该机制的补强。

## Formal main evidence, density 0.15

- Guard-only: success=0.633, cost=0.207, route=0.868.
- Shield-only: success=0.627, cost=0.227, route=0.871.
- Full candidate: success=0.620, cost=0.247, route=0.865.
- Gated risk: success=0.600, cost=0.253, route=0.849.
- Risk-only: success=0.000, cost=0.000, route=0.009; low cost is stagnation, not safe driving.
- No-action-guard: success=0.000, cost=1.000; removing the guard collapses safety.

## Ablation evidence

- No-action-guard collapses to success=0.000 and cost=1.000.
- Removing TTC lowers density-0.15 success to 0.540 and increases cost to 0.360.
- Removing lane and smooth terms worsens trade-offs but does not overturn the action-guard mechanism.

## Robustness evidence

- Stress density 0.20: shield-only success=0.480, gated risk success=0.447, retuned full success=0.453.
- Stress density 0.25: guard-only remains the cleanest survivor, success=0.267, cost=0.487.
- External seeds at density 0.15: shield-only success=0.687 [0.632,0.737], gated risk success=0.663 [0.608,0.714]; intervals overlap, so no superiority claim.

## Parameter sensitivity closure

- TTC14/v18: density-0.15 success=0.573, cost=0.260; below the 0.60/0.25 promotion gate and kept diagnostic.
- Guard ttc13/v18 and target-speed v19 show mixed seed/density trade-offs and are not promoted.
- Moderate lateral/smooth retune repairs one seed but worsens another; not promoted.
