"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/entities/project.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/entities 的模块。导入/依赖:外部:无；内部:@n8n/typeorm；本地:./abstract-entity、./project-relation、./shared-credentials、./shared-workflow 等2项。导出:Project。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/entities/project.ts -> services/n8n/infrastructure/n8n-db/persistence/models/project.py

import { Column, Entity, JoinColumn, ManyToOne, OneToMany, Relation } from '@n8n/typeorm';

import { WithTimestampsAndStringId } from './abstract-entity';
import type { ProjectRelation } from './project-relation';
import type { SharedCredentials } from './shared-credentials';
import type { SharedWorkflow } from './shared-workflow';
import { User } from './user';
import type { Variables } from './variables';

@Entity()
export class Project extends WithTimestampsAndStringId {
	@Column({ length: 255 })
	name: string;

	@Column({ type: 'varchar', length: 36 })
	type: 'personal' | 'team';

	@Column({ type: 'json', nullable: true })
	icon: { type: 'emoji' | 'icon'; value: string } | null;

	@Column({ type: 'varchar', length: 512, nullable: true })
	description: string | null;

	@OneToMany('ProjectRelation', 'project')
	projectRelations: ProjectRelation[];

	@OneToMany('SharedCredentials', 'project')
	sharedCredentials: SharedCredentials[];

	@OneToMany('SharedWorkflow', 'project')
	sharedWorkflows: SharedWorkflow[];

	@OneToMany('Variables', 'project')
	variables: Variables[];

	@Column({ type: String, nullable: true })
	creatorId: string | null;

	@ManyToOne('User', { onDelete: 'SET NULL' })
	@JoinColumn({ name: 'creatorId' })
	creator?: Relation<User>;
}
