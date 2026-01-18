"""
MIGRATION-META:
  source_path: packages/cli/src/middlewares/list-query/dtos/workflow.sort-by.dto.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/middlewares/list-query/dtos 的工作流模块。导入/依赖:外部:class-validator；内部:无；本地:无。导出:WorkflowSortByParameter、WorkflowSorting。关键函数/方法:validate、defaultMessage。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Middleware -> presentation/api/middleware
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/middlewares/list-query/dtos/workflow.sort-by.dto.ts -> services/n8n/presentation/cli/api/middleware/list-query/dtos/workflow_sort_by_dto.py

import type { ValidatorConstraintInterface, ValidationArguments } from 'class-validator';
import { IsString, Validate, ValidatorConstraint } from 'class-validator';

@ValidatorConstraint({ name: 'WorkflowSortByParameter', async: false })
export class WorkflowSortByParameter implements ValidatorConstraintInterface {
	validate(text: string, _: ValidationArguments) {
		const [column, order] = text.split(':');
		if (!column || !order) return false;

		return ['name', 'createdAt', 'updatedAt'].includes(column) && ['asc', 'desc'].includes(order);
	}

	defaultMessage(_: ValidationArguments) {
		return 'Invalid value for sortBy parameter';
	}
}

export class WorkflowSorting {
	@IsString()
	@Validate(WorkflowSortByParameter)
	sortBy?: string;
}
