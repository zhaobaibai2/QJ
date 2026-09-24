# GuardShield-Runtime V7 投稿前强审稿修改状态

生成时间：2026-07-01 11:54 CST  
远程目录：`/home/aaa/data/qj/risk/paper`

## 已更新的主要文件

- `main.tex`
- `paper.pdf`
- `references.bib`
- `figures/fig1_framework.tex`
- `figures/fig3_primary_tradeoff.tex`
- `tables/table1_protocol.tex`
- `tables/table2_primary_d015.tex`
- `tables/table3_density_sweep.tex`
- `tables/table4_ablation.tex`
- `tables/table5_external_ci.tex`
- `tables/table6_stress.tex`

## 按强审稿意见完成的修改

1. 题目改为 `GuardShield-Runtime: Runtime Action Guarding and Shielding for Progress-Preserving Dense-Traffic Driving`，删除 `Data-Selected` 叙事。
2. Abstract、Introduction、Results、Discussion、Conclusion 围绕 `progress-safety conflict -> runtime action intervention -> simulator-bounded claim` 重写。
3. Method 增加可复现细节：动作管线、progress-gated risk penalty、TTC/speed guard 条件、训练/测试使用方式、Algorithm 1。
4. Experimental Protocol 增补环境、指标、训练预算、held-out split、external-seed 300 episodes、Wilson CI 解释、variant 定义。
5. Related Work 扩充为 safe/constrained RL、runtime shielding/safety filters、closed-loop autonomous driving benchmarks 三条线。
6. 参考文献扩充到 22 篇，并完成 BibTeX 编译。
7. Fig.1 重画为执行管线 + 决策逻辑，Fig.2 改为 formal contrast、zoomed progress-safety frontier、external-seed CI 三联图。
8. Table I 压缩为 evaluation blocks；Table II 改成 Guard/Shield runtime 命名和 delta 列；Table IV 去掉不必要 shading；Table V/VI 改为更谨慎的 caption。
9. 全文术语统一为 `Guard runtime`、`Shield runtime`、`episode-level safety cost rate`、`route completion`、`progress-gated risk penalty`。
10. 禁用/内部报告味表达已审计清理，包括 `This draft`、`remote experiment evidence`、`Data-Selected`、`promotion tables`、`selected formal mode` 等。

## 数据和代码依据

- 实验数据、配置和代码均来自远程 qj 工程：`/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive`。
- 复现性参数从真实 `config.json` 和 `racrl/envs.py` 提取，包括 PPO 训练预算、seed split、TTC threshold、目标速度、hard/soft TTC guard、speed cap、risk penalty 组成。
- 本轮没有重新跑训练或评估；属于论文强审稿级重写、图表重排、引用扩充和已有证据重组织。

## 使用的 skill / 工作流

- 已检查远程 aaa 端可用技能目录，确认存在 `nature-writing`、`nature-polishing`、`nature-figure`、`nature-academic-search`、`paper-spine-*` 等论文写作与审稿工作流。
- 本轮按 `nature-writing` 的论文主线、方法、实验、相关工作和结论结构要求重写正文。
- 本轮按 `nature-polishing` 的学术语气和 claim-boundary 要求清理内部报告式措辞和过度 claim。
- 本轮按 `nature-figure` 的 figure-contract / QA 思路检查 Fig.1、Fig.2 的结论服务性、信息层级、字体和 PDF 渲染。
- 本轮按 `nature-academic-search` 的 source-routing 思路补齐相关工作类别；由于当前可调用环境未暴露 CrossRef/PubMed/arXiv MCP 检索工具，参考文献执行的是类别覆盖与 BibTeX 编译核验，不等同于逐条联网 DOI 核验。

## 验证结果

- `paper.pdf` 已同步到最新 `main.pdf`。
- PDF 页数：7。
- PDF 大小：135367 bytes。
- `references.bib` 条目数：22。
- `xelatex + bibtex + xelatex + xelatex` 编译通过。
- 日志审计未发现 LaTeX Error、Undefined control、undefined references、undefined citations、Overfull。
- PDF 文本审计未发现禁用内部报告词或过度 claim。
- 已渲染并目检第 3-7 页，Fig.1、Fig.2、Table I-VI、Discussion、References 没有明显错位、重叠或空白页错误。

## 仍需注意

- 当前版本因补足方法、协议和 22 篇参考文献扩展为 7 页。如果目标 venue 强制 6 页以内，需要进一步压缩正文或 references。
- 参考文献覆盖已经按主线补齐并可编译，但本轮没有逐篇联网核验 DOI/页码。
- 高密度 `d=0.20/0.25` 仍按边界结果处理，不能写成 solved generalization。
