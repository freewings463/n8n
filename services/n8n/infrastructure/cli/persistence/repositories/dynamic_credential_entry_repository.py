"""
MIGRATION-META:
  source_path: packages/cli/src/modules/dynamic-credentials.ee/database/repositories/dynamic-credential-entry.repository.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/modules/dynamic-credentials.ee/database 的仓储。导入/依赖:外部:无；内部:@n8n/di、@n8n/typeorm；本地:../entities/dynamic-credential-entry。导出:DynamicCredentialEntryRepository。关键函数/方法:无。用于封装该模块数据读写与查询细节，隔离持久层。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected TypeORM Repository/EntityManager usage
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/dynamic-credentials.ee/database/repositories/dynamic-credential-entry.repository.ts -> services/n8n/infrastructure/cli/persistence/repositories/dynamic_credential_entry_repository.py

import { Service } from '@n8n/di';
import { DataSource, Repository } from '@n8n/typeorm';

import { DynamicCredentialEntry } from '../entities/dynamic-credential-entry';

@Service()
export class DynamicCredentialEntryRepository extends Repository<DynamicCredentialEntry> {
	constructor(dataSource: DataSource) {
		super(DynamicCredentialEntry, dataSource.manager);
	}
}
