"""
MIGRATION-META:
  source_path: packages/workflow/src/errors/trigger-close.error.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src/errors 的工作流错误。导入/依赖:外部:无；内部:@n8n/errors；本地:../interfaces。导出:TriggerCloseError。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Workflow errors -> domain/exceptions
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/errors/trigger-close.error.ts -> services/n8n/domain/workflow/exceptions/trigger_close_error.py

import { ApplicationError, type ErrorLevel } from '@n8n/errors';
import type { INode } from '../interfaces';

interface TriggerCloseErrorOptions extends ErrorOptions {
	level: ErrorLevel;
}

export class TriggerCloseError extends ApplicationError {
	constructor(
		readonly node: INode,
		{ cause, level }: TriggerCloseErrorOptions,
	) {
		super('Trigger Close Failed', { cause, extra: { nodeName: node.name } });
		this.level = level;
	}
}
