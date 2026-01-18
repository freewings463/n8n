"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Code/reserved-key-found-error.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Code 的节点。导入/依赖:外部:无；内部:无；本地:./ValidationError。导出:ReservedKeyFoundError。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Code/reserved-key-found-error.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Code/reserved_key_found_error.py

import { ValidationError } from './ValidationError';

export class ReservedKeyFoundError extends ValidationError {
	constructor(reservedKey: string, itemIndex: number) {
		super({
			message: 'Invalid output format',
			description: `An output item contains the reserved key <code>${reservedKey}</code>. To get around this, please wrap each item in an object, under a key called <code>json</code>. <a href="https://docs.n8n.io/data/data-structure/#data-structure" target="_blank">Example</a>`,
			itemIndex,
		});
	}
}
