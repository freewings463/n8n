"""
MIGRATION-META:
  source_path: packages/cli/src/middlewares/list-query/dtos/base.filter.dto.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/middlewares/list-query/dtos 的模块。导入/依赖:外部:class-transformer、class-validator；内部:@n8n/backend-common、n8n-workflow；本地:无。导出:BaseFilter。关键函数/方法:validate、toFilter。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Middleware -> presentation/api/middleware
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/middlewares/list-query/dtos/base.filter.dto.ts -> services/n8n/presentation/cli/api/middleware/list-query/dtos/base_filter_dto.py

import { isObjectLiteral } from '@n8n/backend-common';
import { plainToInstance, instanceToPlain } from 'class-transformer';
import { validate } from 'class-validator';
import { jsonParse, UnexpectedError } from 'n8n-workflow';

export class BaseFilter {
	protected static async toFilter(rawFilter: string, Filter: typeof BaseFilter) {
		const dto = jsonParse(rawFilter, { errorMessage: 'Failed to parse filter JSON' });

		if (!isObjectLiteral(dto)) throw new UnexpectedError('Filter must be an object literal');

		const instance = plainToInstance(Filter, dto, {
			excludeExtraneousValues: true, // remove fields not in class
		});

		await instance.validate();

		return instanceToPlain(instance, {
			exposeUnsetFields: false, // remove in-class undefined fields
		});
	}

	private async validate() {
		const result = await validate(this);

		if (result.length > 0) throw new UnexpectedError('Parsed filter does not fit the schema');
	}
}
