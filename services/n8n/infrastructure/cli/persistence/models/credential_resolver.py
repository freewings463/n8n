"""
MIGRATION-META:
  source_path: packages/cli/src/modules/dynamic-credentials.ee/database/entities/credential-resolver.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/modules/dynamic-credentials.ee/database 的模块。导入/依赖:外部:无；内部:@n8n/db、@n8n/decorators、@n8n/typeorm；本地:无。导出:DynamicCredentialResolver。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/dynamic-credentials.ee/database/entities/credential-resolver.ts -> services/n8n/infrastructure/cli/persistence/models/credential_resolver.py

import { WithTimestampsAndStringId } from '@n8n/db';
import type { CredentialResolverConfiguration } from '@n8n/decorators';
import { Column, Entity } from '@n8n/typeorm';

@Entity()
export class DynamicCredentialResolver extends WithTimestampsAndStringId {
	@Column({ type: 'varchar', length: 128 })
	name: string;

	@Column({ type: 'varchar', length: 128 })
	type: string;

	@Column({ type: 'text' })
	config: string;

	/** Decrypted config, not persisted to the database */
	decryptedConfig?: CredentialResolverConfiguration;
}
