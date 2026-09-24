# ISCSIC 中文草稿工程

生成时间：2026-07-01T09:12:32

## 重要边界

- 这是中文工作稿，便于作者先审逻辑；ISCSIC 官网要求 manuscript written in English，后续投稿前必须转英文。
- 使用官方 ISCSIC Full Paper Template 下载包中的 IEEE LaTeX 模板类。
- 正式论文证据只来自 `n_envs=16` final manifest，不混用历史 n_envs=8/10/32 诊断结果。

## 主文件

- `main_zh.tex`：中文 ISCSIC/IEEE 双栏草稿。
- `main_zh.pdf`：编译后 PDF。
- `figures/`：TikZ/PGFPlots 生成图与复制的定性图。
- `tables/`：主表、消融表、外部种子表。
- `artifacts/`：source map、evidence bank、claim register、figure map、result inventory、writing rationale matrix。

## 编译命令

```bash
cd /home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/iscsic_zh_draft_20260701
xelatex -interaction=nonstopmode -halt-on-error main_zh.tex
bibtex main_zh
xelatex -interaction=nonstopmode -halt-on-error main_zh.tex
xelatex -interaction=nonstopmode -halt-on-error main_zh.tex
```
