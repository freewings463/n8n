"""
MIGRATION-META:
  source_path: packages/cli/src/modules/data-table/data-table.module.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/data-table 的模块。导入/依赖:外部:无；内部:@n8n/decorators、@n8n/di；本地:./data-table.controller、./data-table-aggregate.controller、./data-table-uploads.controller、./data-table.service 等5项。导出:DataTableModule。关键函数/方法:init、shutdown、entities、context。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/data-table/data-table.module.ts -> services/n8n/application/cli/services/modules/data-table/data_table_module.py

import type { ModuleInterface } from '@n8n/decorators';
import { BackendModule, OnShutdown } from '@n8n/decorators';
import { Container } from '@n8n/di';

@BackendModule({ name: 'data-table' })
export class DataTableModule implements ModuleInterface {
	async init() {
		await import('./data-table.controller');
		await import('./data-table-aggregate.controller');
		await import('./data-table-uploads.controller');

		const { DataTableService } = await import('./data-table.service');
		await Container.get(DataTableService).start();

		const { DataTableAggregateService } = await import('./data-table-aggregate.service');
		await Container.get(DataTableAggregateService).start();

		const { DataTableFileCleanupService } = await import('./data-table-file-cleanup.service');
		await Container.get(DataTableFileCleanupService).start();
	}

	@OnShutdown()
	async shutdown() {
		const { DataTableService } = await import('./data-table.service');
		await Container.get(DataTableService).shutdown();

		const { DataTableAggregateService } = await import('./data-table-aggregate.service');
		await Container.get(DataTableAggregateService).shutdown();

		const { DataTableFileCleanupService } = await import('./data-table-file-cleanup.service');
		await Container.get(DataTableFileCleanupService).shutdown();
	}

	async entities() {
		const { DataTable } = await import('./data-table.entity');
		const { DataTableColumn } = await import('./data-table-column.entity');

		return [DataTable, DataTableColumn];
	}

	async context() {
		const { DataTableProxyService } = await import('./data-table-proxy.service');

		return { dataTableProxyProvider: Container.get(DataTableProxyService) };
	}
}
