"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/entities/role.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/entities 的模块。导入/依赖:外部:无；内部:@n8n/typeorm；本地:./abstract-entity、./project-relation、./scope。导出:Role。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/entities/role.ts -> services/n8n/infrastructure/n8n-db/persistence/models/role.py

import { Column, Entity, JoinTable, ManyToMany, OneToMany, PrimaryColumn } from '@n8n/typeorm';

import { WithTimestamps } from './abstract-entity';
import type { ProjectRelation } from './project-relation';
import { Scope } from './scope';

@Entity({
	name: 'role',
})
export class Role extends WithTimestamps {
	@PrimaryColumn({
		type: String,
		name: 'slug',
	})
	slug: string;

	@Column({
		type: String,
		nullable: false,
		name: 'displayName',
	})
	displayName: string;

	@Column({
		type: String,
		nullable: true,
		name: 'description',
	})
	description: string | null;

	@Column({
		type: Boolean,
		default: false,
		name: 'systemRole',
	})
	/**
	 * Indicates if the role is managed by the system and cannot be edited.
	 */
	systemRole: boolean;

	@Column({
		type: String,
		name: 'roleType',
	})
	/**
	 * Type of the role, e.g., global, project, or workflow.
	 */
	roleType: 'global' | 'project' | 'workflow' | 'credential';

	@OneToMany('ProjectRelation', 'role')
	projectRelations: ProjectRelation[];

	@ManyToMany(() => Scope, {
		eager: true,
	})
	@JoinTable({
		name: 'role_scope',
		joinColumn: { name: 'roleSlug', referencedColumnName: 'slug' },
		inverseJoinColumn: { name: 'scopeSlug', referencedColumnName: 'slug' },
	})
	scopes: Scope[];
}
