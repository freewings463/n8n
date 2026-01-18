"""
MIGRATION-META:
  source_path: packages/cli/src/modules/data-table/data-table-size-validator.service.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/data-table 的服务。导入/依赖:外部:无；内部:@n8n/config、@n8n/di、n8n-workflow、@/telemetry；本地:./errors/data-table-validation.error、./utils/size-utils。导出:DataTableSizeValidator。关键函数/方法:shouldRefresh、getCachedSizeData、validateSize、sizeToState、getSizeStatus、reset。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/data-table/data-table-size-validator.service.ts -> services/n8n/application/cli/services/data-table/data_table_size_validator_service.py

import { GlobalConfig } from '@n8n/config';
import { Service } from '@n8n/di';
import { DataTableSizeStatus, DataTablesSizeData } from 'n8n-workflow';

import { Telemetry } from '@/telemetry';

import { DataTableValidationError } from './errors/data-table-validation.error';
import { toMb } from './utils/size-utils';

@Service()
export class DataTableSizeValidator {
	private lastCheck: Date | undefined;
	private cachedSizeData: DataTablesSizeData | undefined;
	private pendingCheck: Promise<DataTablesSizeData> | null = null;

	constructor(
		private readonly globalConfig: GlobalConfig,
		private readonly telemetry: Telemetry,
	) {}

	private shouldRefresh(now: Date): boolean {
		if (
			!this.lastCheck ||
			!this.cachedSizeData ||
			now.getTime() - this.lastCheck.getTime() >= this.globalConfig.dataTable.sizeCheckCacheDuration
		) {
			return true;
		}

		return false;
	}

	async getCachedSizeData(
		fetchSizeDataFn: () => Promise<DataTablesSizeData>,
		now = new Date(),
	): Promise<DataTablesSizeData> {
		// If there's a pending check, wait for it to complete
		if (this.pendingCheck) {
			this.cachedSizeData = await this.pendingCheck;
		} else {
			// Check if we need to refresh the size data
			if (this.shouldRefresh(now)) {
				this.pendingCheck = fetchSizeDataFn();
				try {
					this.cachedSizeData = await this.pendingCheck;
					this.lastCheck = now;
				} finally {
					this.pendingCheck = null;
				}
			}
		}

		return this.cachedSizeData!;
	}

	async validateSize(
		fetchSizeFn: () => Promise<DataTablesSizeData>,
		now = new Date(),
	): Promise<void> {
		const size = await this.getCachedSizeData(fetchSizeFn, now);
		if (size.totalBytes >= this.globalConfig.dataTable.maxSize) {
			this.telemetry.track('User hit data table storage limit', {
				total_bytes: size.totalBytes,
				max_bytes: this.globalConfig.dataTable.maxSize,
			});

			throw new DataTableValidationError(
				`Data table size limit exceeded: ${toMb(size.totalBytes)}MB used, limit is ${toMb(this.globalConfig.dataTable.maxSize)}MB`,
			);
		}
	}

	sizeToState(sizeBytes: number): DataTableSizeStatus {
		const warningThreshold =
			this.globalConfig.dataTable.warningThreshold ??
			Math.floor(0.8 * this.globalConfig.dataTable.maxSize);

		if (sizeBytes >= this.globalConfig.dataTable.maxSize) {
			return 'error';
		} else if (sizeBytes >= warningThreshold) {
			return 'warn';
		}
		return 'ok';
	}

	async getSizeStatus(fetchSizeFn: () => Promise<DataTablesSizeData>, now = new Date()) {
		const size = await this.getCachedSizeData(fetchSizeFn, now);
		return this.sizeToState(size.totalBytes);
	}

	reset() {
		this.lastCheck = undefined;
		this.cachedSizeData = undefined;
		this.pendingCheck = null;
	}
}
