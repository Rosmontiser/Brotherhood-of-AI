# 📚 Week 03 · 论文解读（DETR 系列）

## 1) DAB-DETR

- 论文 PDF：[`DAB-DETR.pdf`](./DAB-DETR.pdf)
- 一句话结论：**DAB-DETR 用动态锚框作为 query，缓解 DETR 训练收敛慢的问题。**

### 核心贡献

1. 将 query 显式参数化为框坐标。  
2. 层间动态更新锚框，优化 query-feature 对齐。  
3. 以更明确的位置先验提升训练稳定性与效率。

### 启发与可复用点

- 证明了“query 设计”是 DETR 性能与收敛速度的关键杠杆。

---

## 2) DN-DETR

- 论文 PDF：[`DN-DETR.pdf`](./DN-DETR.pdf)
- 一句话结论：**DN-DETR 通过 denoising 训练降低匹配学习难度，显著加速 DETR 收敛。**

### 核心贡献

1. 提出噪声 GT 重构任务，稳定早期训练。  
2. 可插拔、改动小，便于迁移到其他 DETR 变体。  
3. 在相同训练预算下获得更高 AP。

### 启发与可复用点

- 工程上非常友好：低成本引入、收益稳定。

---

## 3) DINO

- 论文 PDF：[`DINO.pdf`](./DINO.pdf)
- 一句话结论：**DINO 综合了 denoising、query 初始化与 box 预测策略，成为 DETR 系列强基线。**

### 核心贡献

1. 对 DN 训练做对比式增强。  
2. 混合 query 选择提升初始化质量。  
3. Look-forward twice 机制优化框预测。  
4. 在收敛速度与精度上达到更优平衡。

### 启发与可复用点

- 若要做端到端检测，DINO 常是“首选起点”。

---

## 4) Mask DINO

- 论文 PDF：[`MaskDINO.pdf`](./MaskDINO.pdf)
- 一句话结论：**Mask DINO 将 DINO 扩展到检测+分割统一框架，兼顾 box 与 mask 预测。**

### 核心贡献

1. 在统一架构内支持多任务（检测、实例分割等）。  
2. 继承 DINO 的训练优势与泛化能力。  
3. 提升了从“检测”走向“像素级理解”的可迁移性。

### 启发与可复用点

- 对需要同时输出框与掩码的场景（自动标注、内容理解）非常实用。

---

## 本周总结

Week 03 主线非常清晰：  
**DAB-DETR（query 形式）→ DN-DETR（训练策略）→ DINO（系统集成）→ Mask DINO（任务扩展）**。  
这是 DETR 走向“更快收敛 + 更强性能 + 更广任务覆盖”的典型演化链。
