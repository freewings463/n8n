---
doc_type: migration_batch
batch_id: "2026-01-18-system-analysis-ddd-mapping"
date: "2026-01-18"
owner: "TBD"
base_commit: "TBD"
status: planned
scope:
  bounded_contexts: ["(auto from packages/*)"]
  layers: ["Domain", "Application", "Interface", "Infrastructure"]
---

# 系统分析 → DDD 四层映射（计划批次）

## 1. 目标与非目标（Goals / Non-goals）

- Goals：基于 `系统分析.md` 的职责摘要，生成文件级 old_path→new_path 映射，用于后续 DDD 预重构迁移。
- Non-goals：本批次不移动任何代码文件、不修改业务逻辑、不做依赖收敛。

## 2. 依赖分析摘要

- 本批次仅生成映射文档，未进行依赖图构建（后续迁移批次需补齐依赖分析与顺序）。

## 3. 变更清单（映射产物）

| old_path | new_path | target_context | target_layer | reason | confidence |
|---------|----------|---------------|--------------|--------|------------|
| （见 mapping-matrix.md 文件级映射清单） | `docs/migration/mapping-matrix.md` | （自动） | （四层） | 自动规则映射 | `Medium` |

## 4. 验证结果

- 编译/启动：N/A（未移动代码）。
- 测试：N/A（未移动代码）。
- 架构约束：N/A（未迁移，后续批次补齐）。
- 性能基线：N/A。

## 5. 决策记录（Decisions）与遗留问题（Open Issues）

- Decisions：按 `packages/<pkg>`（或 `packages/@n8n/<pkg>`）作为默认限界上下文名来源，映射到 `services/{context}/...`。
- Open Issues：该规则为启发式；需对 `packages/cli`、`packages/core` 等混层包进行人工复核与拆分策略。

## 6. 回退方案（Rollback）

- 删除本批次生成的文档文件即可回退（无代码变更）。

## 7. 下一批计划（Next）

- 对高风险目录（例如 `packages/cli/src/services/**`）补充依赖分析与更细粒度的用例/领域划分。
- 产出首个真实迁移批次：从叶子节点（依赖最少）开始 `git mv`。

## 附录：统计

- 源分析生成时间：2026-01-18 10:45:03
- 文件条目总数：5739
- Layer 统计：{'Infrastructure': 4070, 'Application': 1223, 'Domain': 189, 'Interface': 257}
- Context Top10：{'nodes-base': 3054, 'cli': 703, 'n8n-nodes-langchain': 458, 'n8n-db': 353, 'n8n-ai-workflow-builder-ee': 209, 'testing': 150, 'n8n-api-types': 132, 'core': 125, 'workflow': 101, 'n8n-node-cli': 73}
