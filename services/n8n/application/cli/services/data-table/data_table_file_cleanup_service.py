"""
MIGRATION-META:
  source_path: packages/cli/src/modules/data-table/data-table-file-cleanup.service.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/data-table 的服务。导入/依赖:外部:无；内部:@n8n/backend-common、@n8n/config、@n8n/di；本地:无。导出:DataTableFileCleanupService。关键函数/方法:start、isErrnoException、typeof、shutdown、clearInterval、cleanupOrphanedFiles、deleteFile。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/data-table/data-table-file-cleanup.service.ts -> services/n8n/application/cli/services/data-table/data_table_file_cleanup_service.py

import { safeJoinPath } from '@n8n/backend-common';
import { GlobalConfig } from '@n8n/config';
import { Service } from '@n8n/di';
import { promises as fs } from 'fs';

@Service()
export class DataTableFileCleanupService {
	private readonly uploadDir: string;

	private cleanupInterval?: NodeJS.Timeout;

	constructor(private readonly globalConfig: GlobalConfig) {
		this.uploadDir = this.globalConfig.dataTable.uploadDir;
	}

	private isErrnoException(error: unknown): error is NodeJS.ErrnoException {
		return (
			typeof error === 'object' &&
			error !== null &&
			'code' in error &&
			typeof (error as { code: unknown }).code === 'string'
		);
	}

	async start() {
		// Run cleanup periodically to delete orphaned files
		this.cleanupInterval = setInterval(() => {
			void this.cleanupOrphanedFiles();
		}, this.globalConfig.dataTable.cleanupIntervalMs);
	}

	async shutdown() {
		if (this.cleanupInterval) {
			clearInterval(this.cleanupInterval);
			this.cleanupInterval = undefined;
		}
	}

	/**
	 * Cleans up orphaned CSV files that exceed the configured maximum age
	 * These are files that were uploaded but never used to create a data table
	 */
	private async cleanupOrphanedFiles(): Promise<void> {
		try {
			const files = await fs.readdir(this.uploadDir);
			const now = Date.now();
			const maxAge = this.globalConfig.dataTable.fileMaxAgeMs;

			for (const file of files) {
				const filePath = safeJoinPath(this.uploadDir, file);
				try {
					const stats = await fs.stat(filePath);
					const fileAge = now - stats.mtimeMs;

					// Delete files older than the configured maximum age
					if (fileAge > maxAge) {
						await fs.unlink(filePath);
					}
				} catch (error) {
					// Ignore errors for individual files (e.g., file already deleted)
					continue;
				}
			}
		} catch (error) {
			// Ignore errors if upload directory doesn't exist yet
			if (!this.isErrnoException(error) || error.code !== 'ENOENT') {
				// Log other errors but don't throw - cleanup is best effort
				console.error('Error cleaning up orphaned CSV files:', error);
			}
		}
	}

	/**
	 * Deletes a specific CSV file by its fileId
	 */
	async deleteFile(fileId: string): Promise<void> {
		const filePath = safeJoinPath(this.uploadDir, fileId);
		try {
			await fs.unlink(filePath);
		} catch (error) {
			// Ignore errors if file doesn't exist
			if (!this.isErrnoException(error) || error.code !== 'ENOENT') {
				throw error;
			}
		}
	}
}
