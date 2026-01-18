"""
MIGRATION-META:
  source_path: packages/cli/src/middlewares/list-query/dtos/credentials.filter.dto.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/middlewares/list-query/dtos 的模块。导入/依赖:外部:class-transformer、class-validator；内部:无；本地:./base.filter.dto。导出:CredentialsFilter。关键函数/方法:fromString。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Middleware -> presentation/api/middleware
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/middlewares/list-query/dtos/credentials.filter.dto.ts -> services/n8n/presentation/cli/api/middleware/list-query/dtos/credentials_filter_dto.py

import { Expose } from 'class-transformer';
import { IsOptional, IsString } from 'class-validator';

import { BaseFilter } from './base.filter.dto';

export class CredentialsFilter extends BaseFilter {
	@IsString()
	@IsOptional()
	@Expose()
	name?: string;

	@IsString()
	@IsOptional()
	@Expose()
	type?: string;

	@IsString()
	@IsOptional()
	@Expose()
	projectId?: string;

	static async fromString(rawFilter: string) {
		return await this.toFilter(rawFilter, CredentialsFilter);
	}
}
