# Citation Verification Report

generated_at: 2026-07-02T12:50:33+0800
workflow: final manuscript citation audit using BibTeX key checks plus public scholarly-source lookup for the newly added recent references.

## Summary

- bibliography entries in `references.bib`: 37
- citation keys missing from `references.bib`: 0
- bibliography entries not cited in `main.tex`: 0
- LaTeX undefined citation warnings after final compile: 0
- known fabricated or unresolved references: 0

## Recently Added References Checked

| key | status | source checked | metadata action |
|---|---|---|---|
| wachi2024constraint | verified | IJCAI 2024 proceedings and DOI page `10.24963/ijcai.2024/913` | retained IJCAI venue, pages 8262--8271, DOI |
| ji2024omnisafe | verified | JMLR volume 25, paper 285 page | retained JMLR metadata, volume, number, pages, URL |
| miller2024optimal | verified | ACM/IEEE ICCPS 2024 DOI page `10.1109/ICCPS61052.2024.00013` | retained ICCPS venue, pages 67--76, DOI |
| feng2023dense | verified | Nature/PubMed metadata for `10.1038/s41586-023-05732-2` | retained Nature volume 615, issue 7953, pages 620--627, DOI |
| jia2024bench2drive | verified | NeurIPS 2024 Datasets and Benchmarks paper and arXiv page `2406.03877` | retained NeurIPS venue and arXiv URL; avoided the NeurIPS URL with underscores because the Springer BibTeX style rendered it incorrectly |

## Compile and Consistency Checks

- `latexmk -pdf -interaction=nonstopmode main.tex` completed successfully.
- `main.log` contains no undefined citation or undefined reference warnings after the final run.
- Remote key check reports no missing citation keys and no unused BibTeX entries.
- URLs containing underscores were avoided in the printed bibliography to prevent Springer `.bst` URL rendering errors.


## Final Polish Audit (2026-07-02T13:10:29+0800)

- Recompiled with `latexmk -pdf -interaction=nonstopmode main.tex`; output remains 32 pages.
- Bibliography is generated from `references.bib` using Springer `sn-mathphys-ay.bst`; `main.tex` contains `\bibliography{references}` and no manual `thebibliography` block.
- Citation-key audit after the final polish reports 37 BibTeX entries, 37 cited keys, 0 missing keys, and 0 unused entries.
- Public-source spot checks reconfirmed the newly added recent references: Wachi et al. 2024/IJCAI, Ji et al. 2024/JMLR OmniSafe, Miller et al. 2024/ICCPS, Feng et al. 2023/Nature, and Jia et al. 2024/NeurIPS Bench2Drive.

## Remaining Caution

The current BibTeX is source-backed and compile-clean. Before final non-anonymous submission, repository or archival DOI fields should be updated if the venue requires public data/code links at acceptance.
