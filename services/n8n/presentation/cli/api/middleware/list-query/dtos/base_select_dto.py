"""
MIGRATION-META:
  source_path: packages/cli/src/middlewares/list-query/dtos/base.select.dto.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/middlewares/list-query/dtos 的模块。导入/依赖:外部:无；内部:@n8n/db、n8n-workflow；本地:无。导出:BaseSelect。关键函数/方法:toSelect。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Middleware -> presentation/api/middleware
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/middlewares/list-query/dtos/base.select.dto.ts -> services/n8n/presentation/cli/api/middleware/list-query/dtos/base_select_dto.py

import { isStringArray } from '@n8n/db';
import { jsonParse, UnexpectedError } from 'n8n-workflow';

export class BaseSelect {
	static selectableFields: Set<string>;

	protected static toSelect(rawFilter: string, Select: typeof BaseSelect) {
		const dto = jsonParse(rawFilter, { errorMessage: 'Failed to parse filter JSON' });

		if (!isStringArray(dto)) throw new UnexpectedError('Parsed select is not a string array');

		return dto.reduce<Record<string, true>>((acc, field) => {
			if (!Select.selectableFields.has(field)) return acc;
			return (acc[field] = true), acc;
		}, {});
	}
}
