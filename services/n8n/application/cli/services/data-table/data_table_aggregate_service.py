"""
MIGRATION-META:
  source_path: packages/cli/src/modules/data-table/data-table-aggregate.service.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/data-table 的服务。导入/依赖:外部:无；内部:@n8n/api-types、@n8n/backend-common、@n8n/db、@n8n/di、@/services/project.service.ee、@n8n/permissions；本地:./data-table.repository。导出:DataTableAggregateService。关键函数/方法:start、shutdown、getManyAndCount。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/data-table/data-table-aggregate.service.ts -> services/n8n/application/cli/services/data-table/data_table_aggregate_service.py

import type { ListDataTableQueryDto } from '@n8n/api-types';
import { Logger } from '@n8n/backend-common';
import { User } from '@n8n/db';
import { Service } from '@n8n/di';

import { ProjectService } from '@/services/project.service.ee';

import { DataTableRepository } from './data-table.repository';
import { hasGlobalScope } from '@n8n/permissions';

@Service()
export class DataTableAggregateService {
	constructor(
		private readonly dataTableRepository: DataTableRepository,
		private readonly projectService: ProjectService,
		private readonly logger: Logger,
	) {
		this.logger = this.logger.scoped('data-table');
	}
	async start() {}
	async shutdown() {}

	async getManyAndCount(user: User, options: ListDataTableQueryDto) {
		if (hasGlobalScope(user, 'dataTable:listProject')) {
			return await this.dataTableRepository.getManyAndCount(options);
		}

		const projects = await this.projectService.getProjectRelationsForUser(user);

		let projectIds = projects.map((x) => x.projectId);
		if (options.filter?.projectId) {
			const mask = [options.filter?.projectId].flat();
			projectIds = projectIds.filter((x) => mask.includes(x));
		}

		if (projectIds.length === 0) {
			return { count: 0, data: [] };
		}

		return await this.dataTableRepository.getManyAndCount({
			...options,
			filter: {
				...options.filter,
				projectId: projectIds,
			},
		});
	}
}
