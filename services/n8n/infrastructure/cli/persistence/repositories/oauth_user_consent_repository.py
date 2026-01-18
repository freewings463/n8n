"""
MIGRATION-META:
  source_path: packages/cli/src/modules/mcp/database/repositories/oauth-user-consent.repository.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/modules/mcp/database 的OAuth仓储。导入/依赖:外部:无；内部:@n8n/di、@n8n/typeorm；本地:../entities/oauth-user-consent.entity。导出:UserConsentRepository。关键函数/方法:findByUserWithClient。用于封装OAuth数据读写与查询细节，隔离持久层。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected TypeORM Repository/EntityManager usage
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/mcp/database/repositories/oauth-user-consent.repository.ts -> services/n8n/infrastructure/cli/persistence/repositories/oauth_user_consent_repository.py

import { Service } from '@n8n/di';
import { DataSource, Repository } from '@n8n/typeorm';

import { UserConsent } from '../entities/oauth-user-consent.entity';

@Service()
export class UserConsentRepository extends Repository<UserConsent> {
	constructor(dataSource: DataSource) {
		super(UserConsent, dataSource.manager);
	}

	/**
	 * Find all consents for a user with client information
	 */
	async findByUserWithClient(userId: string): Promise<UserConsent[]> {
		return await this.find({
			where: { userId },
			relations: ['client'],
			order: { grantedAt: 'DESC' },
		});
	}
}
