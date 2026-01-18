"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/entities/auth-identity.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/entities 的模块。导入/依赖:外部:无；内部:@n8n/typeorm；本地:./abstract-entity、./types-db、./user。导出:AuthIdentity。关键函数/方法:create。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/entities/auth-identity.ts -> services/n8n/infrastructure/n8n-db/persistence/models/auth_identity.py

import { Column, Entity, ManyToOne, PrimaryColumn, Unique } from '@n8n/typeorm';

import { WithTimestamps } from './abstract-entity';
import { AuthProviderType } from './types-db';
import { User } from './user';

@Entity()
@Unique(['providerId', 'providerType'])
export class AuthIdentity extends WithTimestamps {
	@Column()
	userId: string;

	@ManyToOne(
		() => User,
		(user) => user.authIdentities,
	)
	user: User;

	@PrimaryColumn()
	providerId: string;

	@PrimaryColumn()
	providerType: AuthProviderType;

	static create(
		user: User,
		providerId: string,
		providerType: AuthProviderType = 'ldap',
	): AuthIdentity {
		const identity = new AuthIdentity();
		identity.user = user;
		identity.userId = user.id;
		identity.providerId = providerId;
		identity.providerType = providerType;
		return identity;
	}
}
