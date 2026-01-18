"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/entities/credentials-entity.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/entities 的模块。导入/依赖:外部:class-validator；内部:@n8n/typeorm；本地:./abstract-entity、./shared-credentials、./types-db。导出:CredentialsEntity。关键函数/方法:toJSON。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/entities/credentials-entity.ts -> services/n8n/infrastructure/n8n-db/persistence/models/credentials_entity.py

import { Column, Entity, Index, OneToMany } from '@n8n/typeorm';
import { IsObject, IsString, Length } from 'class-validator';

import { WithTimestampsAndStringId } from './abstract-entity';
import type { SharedCredentials } from './shared-credentials';
import type { ICredentialsDb } from './types-db';

@Entity()
export class CredentialsEntity extends WithTimestampsAndStringId implements ICredentialsDb {
	@Column({ length: 128 })
	@IsString({ message: 'Credential `name` must be of type string.' })
	@Length(3, 128, {
		message: 'Credential name must be $constraint1 to $constraint2 characters long.',
	})
	name: string;

	@Column('text')
	@IsObject()
	data: string;

	@Index()
	@IsString({ message: 'Credential `type` must be of type string.' })
	@Column({
		length: 128,
	})
	type: string;

	@OneToMany('SharedCredentials', 'credentials')
	shared: SharedCredentials[];

	/**
	 * Whether the credential is managed by n8n. We currently use this flag
	 * to provide OpenAI free credits on cloud. Managed credentials cannot be
	 * edited by the user.
	 */
	@Column({ default: false })
	isManaged: boolean;

	/**
	 * Whether the credential is available for use by all users.
	 */
	@Column({ default: false })
	isGlobal: boolean;

	/**
	 * Whether the credential can be dynamically resolved by a resolver.
	 */
	@Column({ default: false })
	isResolvable: boolean;

	/**
	 * Whether the credential resolver should allow falling back to static credentials
	 * if dynamic resolution fails.
	 */
	@Column({ default: false })
	resolvableAllowFallback: boolean;

	/**
	 * ID of the dynamic credential resolver associated with this credential.
	 */
	@Column({ type: 'varchar', nullable: true })
	resolverId: string | null;

	toJSON() {
		const { shared, ...rest } = this;
		return rest;
	}
}
