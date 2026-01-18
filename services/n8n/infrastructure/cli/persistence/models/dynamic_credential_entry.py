"""
MIGRATION-META:
  source_path: packages/cli/src/modules/dynamic-credentials.ee/database/entities/dynamic-credential-entry.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/modules/dynamic-credentials.ee/database 的模块。导入/依赖:外部:无；内部:@n8n/db、@n8n/typeorm；本地:./credential-resolver。导出:DynamicCredentialEntry。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/dynamic-credentials.ee/database/entities/dynamic-credential-entry.ts -> services/n8n/infrastructure/cli/persistence/models/dynamic_credential_entry.py

import { CredentialsEntity, WithTimestamps } from '@n8n/db';
import { Column, Entity, JoinColumn, ManyToOne, PrimaryColumn } from '@n8n/typeorm';

import { DynamicCredentialResolver } from './credential-resolver';

@Entity({
	name: 'dynamic_credential_entry',
})
export class DynamicCredentialEntry extends WithTimestamps {
	constructor() {
		super();
	}

	@PrimaryColumn({
		name: 'credential_id',
	})
	credentialId: string;

	@PrimaryColumn({
		name: 'subject_id',
	})
	subjectId: string;

	@PrimaryColumn({
		name: 'resolver_id',
	})
	resolverId: string;

	@Column('text')
	data: string;

	@ManyToOne(() => CredentialsEntity, { onDelete: 'CASCADE' })
	@JoinColumn({ name: 'credential_id' })
	credential: CredentialsEntity;

	@ManyToOne(() => DynamicCredentialResolver, { onDelete: 'CASCADE' })
	@JoinColumn({ name: 'resolver_id' })
	resolver: DynamicCredentialResolver;
}
