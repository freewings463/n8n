"""
MIGRATION-META:
  source_path: packages/@n8n/config/src/configs/data-table.config.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/config/src/configs 的配置。导入/依赖:外部:无；内部:无；本地:../decorators。导出:DataTableConfig。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/config treated as infrastructure configuration/runtime environment
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/config/src/configs/data-table.config.ts -> services/n8n/infrastructure/n8n-config/configuration/configs/data_table_config.py

import { tmpdir } from 'node:os';
import path from 'node:path';

import { Config, Env } from '../decorators';

@Config
export class DataTableConfig {
	/** Specifies the maximum allowed size (in bytes) for data tables. */
	@Env('N8N_DATA_TABLES_MAX_SIZE_BYTES')
	maxSize: number = 50 * 1024 * 1024;

	/**
	 * The percentage threshold at which a warning is triggered for data tables.
	 * When the usage of a data table reaches or exceeds this value, a warning is issued.
	 * Defaults to 80% of maxSize if not explicitly set via environment variable.
	 */
	@Env('N8N_DATA_TABLES_WARNING_THRESHOLD_BYTES')
	warningThreshold?: number;

	/**
	 * The duration in milliseconds for which the data table size is cached.
	 * This prevents excessive database queries for size validation.
	 */
	@Env('N8N_DATA_TABLES_SIZE_CHECK_CACHE_DURATION_MS')
	sizeCheckCacheDuration: number = 5 * 1000;

	/**
	 * The maximum allowed file size (in bytes) for CSV uploads to data tables.
	 * If set, this is the hard limit for file uploads.
	 * If not set, the upload limit will be the remaining available storage space.
	 */
	@Env('N8N_DATA_TABLES_UPLOAD_MAX_FILE_SIZE_BYTES')
	uploadMaxFileSize?: number;

	/**
	 * The interval in milliseconds at which orphaned uploaded files are cleaned up.
	 * Defaults to 60 seconds if not explicitly set via environment variable.
	 */
	@Env('N8N_DATA_TABLES_CLEANUP_INTERVAL_MS')
	cleanupIntervalMs: number = 60 * 1000;

	/**
	 * The maximum age in milliseconds for uploaded files before they are considered orphaned and deleted.
	 * Files older than this threshold are removed during cleanup.
	 * Defaults to 2 minutes if not explicitly set via environment variable.
	 */
	@Env('N8N_DATA_TABLES_FILE_MAX_AGE_MS')
	fileMaxAgeMs: number = 2 * 60 * 1000;

	/**
	 * The directory path where uploaded CSV files are temporarily stored before being imported.
	 * Files in this directory are automatically cleaned up after a configurable period (fileMaxAgeMs).
	 * Computed as: <system-tmp-dir>/n8nDataTableUploads
	 * Example: /tmp/n8nDataTableUploads
	 */
	readonly uploadDir: string;

	constructor() {
		this.uploadDir = path.join(tmpdir(), 'n8nDataTableUploads');
	}
}
