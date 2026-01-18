"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/entities/auth-provider-sync-history.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/entities 的模块。导入/依赖:外部:无；内部:@n8n/typeorm；本地:./abstract-entity、./types-db。导出:AuthProviderSyncHistory。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/entities/auth-provider-sync-history.ts -> services/n8n/infrastructure/n8n-db/persistence/models/auth_provider_sync_history.py

import { Column, Entity, PrimaryGeneratedColumn } from '@n8n/typeorm';

import { DateTimeColumn } from './abstract-entity';
import { AuthProviderType, RunningMode, SyncStatus } from './types-db';

@Entity()
export class AuthProviderSyncHistory {
	@PrimaryGeneratedColumn()
	id: number;

	@Column('text')
	providerType: AuthProviderType;

	@Column('text')
	runMode: RunningMode;

	@Column('text')
	status: SyncStatus;

	@DateTimeColumn()
	startedAt: Date;

	@DateTimeColumn()
	endedAt: Date;

	@Column()
	scanned: number;

	@Column()
	created: number;

	@Column()
	updated: number;

	@Column()
	disabled: number;

	@Column()
	error: string;
}
