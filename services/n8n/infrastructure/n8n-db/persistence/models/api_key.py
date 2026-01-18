"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/entities/api-key.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/entities 的模块。导入/依赖:外部:无；内部:@n8n/permissions、@n8n/typeorm、n8n-workflow；本地:./abstract-entity、./user。导出:ApiKey。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/entities/api-key.ts -> services/n8n/infrastructure/n8n-db/persistence/models/api_key.py

import type { ApiKeyScope } from '@n8n/permissions';
import { Column, Entity, Index, ManyToOne, Unique } from '@n8n/typeorm';
import { ApiKeyAudience } from 'n8n-workflow';

import { JsonColumn, WithTimestampsAndStringId } from './abstract-entity';
import { User } from './user';

@Entity('user_api_keys')
@Unique(['userId', 'label'])
export class ApiKey extends WithTimestampsAndStringId {
	@ManyToOne(
		() => User,
		(user) => user.id,
		{ onDelete: 'CASCADE' },
	)
	user: User;

	@Column({ type: String })
	userId: string;

	@Column({ type: String })
	label: string;

	@JsonColumn({ nullable: false })
	scopes: ApiKeyScope[];

	@Index({ unique: true })
	@Column({ type: String })
	apiKey: string;

	@Column({ type: String, default: 'public-api' })
	audience: ApiKeyAudience;
}
