"""
MIGRATION-META:
  source_path: packages/cli/src/middlewares/list-query/dtos/workflow.select.dto.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/middlewares/list-query/dtos 的工作流模块。导入/依赖:外部:无；内部:无；本地:./base.select.dto。导出:WorkflowSelect。关键函数/方法:fromString。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Middleware -> presentation/api/middleware
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/middlewares/list-query/dtos/workflow.select.dto.ts -> services/n8n/presentation/cli/api/middleware/list-query/dtos/workflow_select_dto.py

import { BaseSelect } from './base.select.dto';

export class WorkflowSelect extends BaseSelect {
	static get selectableFields() {
		return new Set([
			'id', // always included downstream
			'name',
			'active',
			'activeVersionId',
			'tags',
			'createdAt',
			'updatedAt',
			'versionId',
			'ownedBy', // non-entity field
			'parentFolder',
			'nodes',
			'isArchived',
			'description',
		]);
	}

	static fromString(rawFilter: string) {
		return this.toSelect(rawFilter, WorkflowSelect);
	}
}
