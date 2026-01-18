"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/entities/folder.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/entities 的模块。导入/依赖:外部:无；内部:无；本地:./abstract-entity、./project、./tag-entity、./workflow-entity。导出:Folder。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/entities/folder.ts -> services/n8n/infrastructure/n8n-db/persistence/models/folder.py

import {
	Column,
	Entity,
	JoinColumn,
	JoinTable,
	ManyToMany,
	ManyToOne,
	OneToMany,
} from '@n8n/typeorm';

import { WithTimestampsAndStringId } from './abstract-entity';
import { Project } from './project';
import { TagEntity } from './tag-entity';
import type { WorkflowEntity } from './workflow-entity';

@Entity()
export class Folder extends WithTimestampsAndStringId {
	@Column()
	name: string;

	@Column({ nullable: true })
	parentFolderId: string | null;

	@ManyToOne(() => Folder, { nullable: true, onDelete: 'CASCADE' })
	@JoinColumn({ name: 'parentFolderId' })
	parentFolder: Folder | null;

	@OneToMany(
		() => Folder,
		(folder) => folder.parentFolder,
	)
	subFolders: Folder[];

	@ManyToOne(() => Project)
	@JoinColumn({ name: 'projectId' })
	homeProject: Project;

	@OneToMany('WorkflowEntity', 'parentFolder')
	workflows: WorkflowEntity[];

	@ManyToMany(() => TagEntity)
	@JoinTable({
		name: 'folder_tag',
		joinColumn: {
			name: 'folderId',
			referencedColumnName: 'id',
		},
		inverseJoinColumn: {
			name: 'tagId',
			referencedColumnName: 'id',
		},
	})
	tags: TagEntity[];
}
