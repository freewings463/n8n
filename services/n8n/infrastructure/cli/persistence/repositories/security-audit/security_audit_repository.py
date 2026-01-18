"""
MIGRATION-META:
  source_path: packages/cli/src/security-audit/security-audit.repository.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/security-audit 的仓储。导入/依赖:外部:无；内部:@n8n/di、@n8n/typeorm、@/modules/…/installed-packages.entity；本地:无。导出:PackagesRepository。关键函数/方法:无。用于封装该模块数据读写与查询细节，隔离持久层。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected TypeORM Repository/EntityManager usage
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/security-audit/security-audit.repository.ts -> services/n8n/infrastructure/cli/persistence/repositories/security-audit/security_audit_repository.py

import { Service } from '@n8n/di';
// eslint-disable-next-line n8n-local-rules/misplaced-n8n-typeorm-import
import { DataSource, Repository } from '@n8n/typeorm';

import { InstalledPackages } from '@/modules/community-packages/installed-packages.entity';

@Service()
export class PackagesRepository extends Repository<InstalledPackages> {
	constructor(dataSource: DataSource) {
		super(InstalledPackages, dataSource.manager);
	}
}
