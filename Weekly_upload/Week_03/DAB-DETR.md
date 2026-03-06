# DAB-DETR 论文简介与解读

- 原论文 PDF：[`DAB-DETR.pdf`](./DAB-DETR.pdf)

## 1. 一句话结论
DAB-DETR 通过动态锚框 query 显著改善 DETR 收敛速度与定位学习效率。

## 2. 关键思路图
```mermaid
flowchart LR
A[Anchor Box Query] --> B[Decoder Layer1]
B --> C[更新后的 Box Query]
C --> D[Decoder Layer2]
D --> E[层层细化预测]
```

## 3. 关键贡献
- 显式位置先验；
- query 与目标对齐更稳定；
- 为后续 DETR 系列改进奠定基础。

## 4. 落地建议
适合需要 DETR 框架但训练预算有限的团队。
