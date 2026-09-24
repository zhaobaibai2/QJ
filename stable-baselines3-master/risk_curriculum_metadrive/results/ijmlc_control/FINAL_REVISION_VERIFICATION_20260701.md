# IJMLC final revision verification

- Generated at: 2026-07-01 22:47 CST
- Remote root: `/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive`
- Manuscript PDF: `results/ijmlc_control/manuscript_ijmlc_20260701/main.pdf`
- Working package: `results/ijmlc_control/ijmlc_manuscript_package_20260701.zip`
- Clean source package: `results/ijmlc_control/ijmlc_submission_source_clean_20260701.zip`

## Completed changes

- Kept Fig. 1 unchanged for manual replacement later.
- Added Section 3.5, "Why GuardShield-Runtime is not only a TTC filter", to distinguish the contribution from a plain RSS/TTC rule without overclaiming formal safety.
- Added a compact baseline sanity table showing PPO and PPO-Lagrangian move but terminate unsafely, while Risk-only avoids cost by stopping.
- Softened PPO-Lagrangian wording throughout: it is now a protocol-specific constrained-baseline outcome, not a general failed method.
- Rewrote the Guard/Shield interpretation as a family-level runtime intervention result rather than a strict ranking among independently controlled ablations.
- Made Table 5 explicitly a post-hoc lowest-cost runtime row summary; Fig. 4 remains the primary fixed-variant evidence.
- Added a visible Fig. 5 note and caption language that the TTC-threshold heatmap is an independent rerun, not a Table 3 replication.
- Reorganized Discussion into cybernetic interpretation, evidence support, intervention burden/operating envelope, and limitations/threats to validity.
- Added an intervention-burden discussion that treats high intervention rate as runtime mitigation evidence, not as an ideal deployment property.
- Added reward-hacking/specification-gaming positioning in Related Work with `pan2022reward` and `skalse2022defining`.
- Removed the missing-trace note from the claim-to-evidence table note; trace visualization is mentioned only once as a limitation.
- Converted Table 6 to a non-floating numbered table so it stays after the Section 6.2 evidence-boundary text.
- Compressed Appendix A3 provenance into five columns and strengthened Appendix B's episode-level/seed-variation boundary.
- Retained the clean source directory with only printed table TeX files used by `main.tex`.

## Verification

- `python -m py_compile` passed for both generation scripts.
- `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` completed successfully.
- `main.pdf` has 25 A4 pages and no page rotation.
- Log/content scan found no fatal LaTeX errors, undefined references, undefined citations, overfull hboxes, stale appendix numbering, visible RCPO labels, "less safe" wording, "Training-time penalty fails", internal result paths, engineering-log terms, or unfinished author-contribution placeholders.
- Printed table numbering is now: Table 1--6 in the main text; Table A1--A3, B1--B2, C1, and D1--D2 in the appendix.
- Visual preview checked the baseline sanity table, Fig. 5 independent-rerun note, and Discussion pages; no visible overlap or table overflow was observed.
- Resource watchdog is still running with the active low-memory guard; latest observed MemAvailable was about 21 GiB and GPU free memory about 10934 MiB.

## Remaining boundary

- Step-level qualitative trajectory traces were not fabricated; the manuscript now mentions them once as a qualitative visualization extension outside the present episode-level evidence package.
- Final author contributions and any hand-drawn replacement for Fig. 1 still need to be inserted before formal submission if required by the target venue.
