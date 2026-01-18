"""
MIGRATION-META:
  source_path: packages/cli/src/services/execution-metadata.service.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/services 的执行服务。导入/依赖:外部:无；内部:@n8n/db、@n8n/di；本地:无。导出:ExecutionMetadataService。关键函数/方法:save。用于封装执行业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/services/execution-metadata.service.ts -> services/n8n/application/cli/services/execution_metadata_service.py

import type { ExecutionMetadata } from '@n8n/db';
import { ExecutionMetadataRepository } from '@n8n/db';
import { Service } from '@n8n/di';

@Service()
export class ExecutionMetadataService {
	constructor(private readonly executionMetadataRepository: ExecutionMetadataRepository) {}

	async save(executionId: string, executionMetadata: Record<string, string>): Promise<void> {
		const metadataRows: Array<Pick<ExecutionMetadata, 'executionId' | 'key' | 'value'>> = [];
		for (const [key, value] of Object.entries(executionMetadata)) {
			metadataRows.push({
				executionId,
				key,
				value,
			});
		}

		await this.executionMetadataRepository.upsert(metadataRows, {
			conflictPaths: { executionId: true, key: true },
		});
	}
}
