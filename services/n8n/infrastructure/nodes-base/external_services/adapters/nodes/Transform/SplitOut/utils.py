"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Transform/SplitOut/utils.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Transform/SplitOut 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:FieldsTracker。关键函数/方法:update、add、getHints。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Transform/SplitOut/utils.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Transform/SplitOut/utils.py

import type { NodeExecutionHint } from 'n8n-workflow';

export class FieldsTracker {
	fields: { [key: string]: boolean } = {};

	add(key: string) {
		if (this.fields[key] === undefined) {
			this.fields[key] = false;
		}
	}

	update(key: string, value: boolean) {
		if (!this.fields[key] && value) {
			this.fields[key] = true;
		}
	}

	getHints() {
		const hints: NodeExecutionHint[] = [];

		for (const [field, value] of Object.entries(this.fields)) {
			if (!value) {
				hints.push({
					message: `The field '${field}' wasn't found in any input item`,
					location: 'outputPane',
				});
			}
		}

		return hints;
	}
}
