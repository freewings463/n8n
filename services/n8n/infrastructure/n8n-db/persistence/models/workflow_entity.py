"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/entities/workflow-entity.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/entities 的工作流模块。导入/依赖:外部:class-validator；内部:n8n-workflow；本地:./abstract-entity、./folder、./shared-workflow、./tag-entity 等6项。导出:WorkflowEntity。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/entities/workflow-entity.ts -> services/n8n/infrastructure/n8n-db/persistence/models/workflow_entity.py

import {
	Column,
	Entity,
	Index,
	JoinColumn,
	JoinTable,
	ManyToMany,
	ManyToOne,
	OneToMany,
} from '@n8n/typeorm';
import { Length } from 'class-validator';
import { IConnections, IDataObject, IWorkflowSettings, WorkflowFEMeta } from 'n8n-workflow';
import type { INode } from 'n8n-workflow';

import { JsonColumn, WithTimestampsAndStringId, dbType } from './abstract-entity';
import { type Folder } from './folder';
import type { SharedWorkflow } from './shared-workflow';
import type { TagEntity } from './tag-entity';
import type { TestRun } from './test-run.ee';
import type { ISimplifiedPinData, IWorkflowDb } from './types-db';
import type { WorkflowHistory } from './workflow-history';
import type { WorkflowStatistics } from './workflow-statistics';
import type { WorkflowTagMapping } from './workflow-tag-mapping';
import { objectRetriever, sqlite } from '../utils/transformers';

@Entity()
export class WorkflowEntity extends WithTimestampsAndStringId implements IWorkflowDb {
	// TODO: Add XSS check
	@Index({ unique: true })
	@Length(1, 128, {
		message: 'Workflow name must be $constraint1 to $constraint2 characters long.',
	})
	@Column({ length: 128 })
	name: string;

	@Column({ type: 'text', nullable: true })
	description: string | null;

	/** @deprecated Please rely on `activeVersionId` being not `null` instead. */
	@Column()
	active: boolean;

	/**
	 * Indicates whether the workflow has been soft-deleted (`true`) or not (`false`).
	 *
	 * Archived workflows can be restored (unarchived) or deleted permanently,
	 * and they can still be executed as sub workflow executions, but they
	 * cannot be activated or modified.
	 */
	@Column({ default: false })
	isArchived: boolean;

	@JsonColumn()
	nodes: INode[];

	@JsonColumn()
	connections: IConnections;

	@JsonColumn({ nullable: true })
	settings?: IWorkflowSettings;

	@JsonColumn({
		nullable: true,
		transformer: objectRetriever,
	})
	staticData?: IDataObject;

	@JsonColumn({
		nullable: true,
		transformer: objectRetriever,
	})
	meta?: WorkflowFEMeta;

	@ManyToMany('TagEntity', 'workflows')
	@JoinTable({
		name: 'workflows_tags', // table name for the junction table of this relation
		joinColumn: {
			name: 'workflowId',
			referencedColumnName: 'id',
		},
		inverseJoinColumn: {
			name: 'tagId',
			referencedColumnName: 'id',
		},
	})
	tags?: TagEntity[];

	@OneToMany('WorkflowTagMapping', 'workflows')
	tagMappings: WorkflowTagMapping[];

	@OneToMany('SharedWorkflow', 'workflow')
	shared: SharedWorkflow[];

	@OneToMany('WorkflowStatistics', 'workflow')
	@JoinColumn({ referencedColumnName: 'workflow' })
	statistics: WorkflowStatistics[];

	@Column({
		type: dbType === 'sqlite' ? 'text' : 'json',
		nullable: true,
		transformer: sqlite.jsonColumn,
	})
	pinData?: ISimplifiedPinData;

	@Column({ length: 36 })
	versionId: string;

	@Column({ name: 'activeVersionId', length: 36, nullable: true })
	activeVersionId: string | null;

	@ManyToOne('WorkflowHistory', { nullable: true })
	@JoinColumn({ name: 'activeVersionId', referencedColumnName: 'versionId' })
	activeVersion: WorkflowHistory | null;

	@Column({ default: 1 })
	versionCounter: number;

	// Excludes error and sub-workflow triggers and disabled triggers
	// Used for billing of plans based on trigger count
	@Column({ default: 0 })
	triggerCount: number;

	@ManyToOne('Folder', 'workflows', {
		nullable: true,
		onDelete: 'CASCADE',
	})
	@JoinColumn({ name: 'parentFolderId' })
	parentFolder: Folder | null;

	@OneToMany('TestRun', 'workflow')
	testRuns: TestRun[];
}
