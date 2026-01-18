"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/entities/scope.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/entities 的模块。导入/依赖:外部:无；内部:@n8n/permissions、@n8n/typeorm；本地:无。导出:Scope。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/entities/scope.ts -> services/n8n/infrastructure/n8n-db/persistence/models/scope.py

import type { Scope as ScopeType } from '@n8n/permissions';
import { Column, Entity, PrimaryColumn } from '@n8n/typeorm';

@Entity({
	name: 'scope',
})
export class Scope {
	@PrimaryColumn({
		type: String,
		name: 'slug',
	})
	slug: ScopeType;

	@Column({
		type: String,
		nullable: true,
		name: 'displayName',
	})
	displayName: string | null;

	@Column({
		type: String,
		nullable: true,
		name: 'description',
	})
	description: string | null;
}
