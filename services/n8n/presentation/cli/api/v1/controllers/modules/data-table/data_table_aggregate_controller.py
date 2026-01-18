"""
MIGRATION-META:
  source_path: packages/cli/src/modules/data-table/data-table-aggregate.controller.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/modules/data-table 的控制器。导入/依赖:外部:无；内部:@n8n/api-types、@n8n/db、@n8n/decorators；本地:./data-table-aggregate.service、./data-table.service。导出:DataTableAggregateController。关键函数/方法:listDataTables、getDataTablesSize。用于处理该模块接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected @RestController/@Controller from @n8n/decorators
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/data-table/data-table-aggregate.controller.ts -> services/n8n/presentation/cli/api/v1/controllers/modules/data-table/data_table_aggregate_controller.py

import { ListDataTableQueryDto } from '@n8n/api-types';
import { AuthenticatedRequest } from '@n8n/db';
import { Get, GlobalScope, Query, RestController } from '@n8n/decorators';

import { DataTableAggregateService } from './data-table-aggregate.service';
import { DataTableService } from './data-table.service';

@RestController('/data-tables-global')
export class DataTableAggregateController {
	constructor(
		private readonly dataTableAggregateService: DataTableAggregateService,
		private readonly dataTableService: DataTableService,
	) {}

	@Get('/')
	@GlobalScope('dataTable:list')
	async listDataTables(
		req: AuthenticatedRequest,
		_res: Response,
		@Query payload: ListDataTableQueryDto,
	) {
		return await this.dataTableAggregateService.getManyAndCount(req.user, payload);
	}

	@Get('/limits')
	@GlobalScope('dataTable:list')
	async getDataTablesSize(req: AuthenticatedRequest) {
		return await this.dataTableService.getDataTablesSize(req.user);
	}
}
