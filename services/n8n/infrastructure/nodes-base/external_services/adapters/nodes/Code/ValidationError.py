"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Code/ValidationError.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Code 的节点。导入/依赖:外部:无；内部:@n8n/errors；本地:无。导出:ValidationError。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Code/ValidationError.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Code/ValidationError.py

import { ApplicationError } from '@n8n/errors';

export class ValidationError extends ApplicationError {
	description = '';

	itemIndex: number | undefined = undefined;

	context: { itemIndex: number } | undefined = undefined;

	lineNumber: number | undefined = undefined;

	constructor({
		message,
		description,
		itemIndex,
		lineNumber,
	}: {
		message: string;
		description: string;
		itemIndex?: number;
		lineNumber?: number;
	}) {
		super(message);

		this.lineNumber = lineNumber;
		this.itemIndex = itemIndex;

		if (this.lineNumber !== undefined && this.itemIndex !== undefined) {
			this.message = `${message} [line ${lineNumber}, for item ${itemIndex}]`;
		} else if (this.lineNumber !== undefined) {
			this.message = `${message} [line ${lineNumber}]`;
		} else if (this.itemIndex !== undefined) {
			this.message = `${message} [item ${itemIndex}]`;
		} else {
			this.message = message;
		}

		this.description = description;

		if (this.itemIndex !== undefined) {
			this.context = { itemIndex: this.itemIndex };
		}
	}
}
