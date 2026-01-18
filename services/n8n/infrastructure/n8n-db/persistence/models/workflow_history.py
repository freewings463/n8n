"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/entities/workflow-history.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/entities 的工作流模块。导入/依赖:外部:无；内部:@n8n/typeorm、n8n-workflow；本地:./abstract-entity、./workflow-entity、./workflow-publish-history。导出:WorkflowHistory。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/entities/workflow-history.ts -> services/n8n/infrastructure/n8n-db/persistence/models/workflow_history.py

import { Column, Entity, ManyToOne, OneToMany, PrimaryColumn, Relation } from '@n8n/typeorm';
import { IConnections } from 'n8n-workflow';
import type { INode } from 'n8n-workflow';

import { JsonColumn, WithTimestamps } from './abstract-entity';
import { WorkflowEntity } from './workflow-entity';
import type { WorkflowPublishHistory } from './workflow-publish-history';

@Entity()
export class WorkflowHistory extends WithTimestamps {
	@PrimaryColumn()
	versionId: string;

	@Column()
	workflowId: string;

	@JsonColumn()
	nodes: INode[];

	@JsonColumn()
	connections: IConnections;

	@Column()
	authors: string;

	@Column({ type: 'text', nullable: true })
	name: string | null;

	@Column({ type: 'text', nullable: true })
	description: string | null;

	@Column({ default: false })
	autosaved: boolean;

	@ManyToOne('WorkflowEntity', {
		onDelete: 'CASCADE',
	})
	workflow: WorkflowEntity;

	@OneToMany('WorkflowPublishHistory', 'workflowHistory')
	workflowPublishHistory: Relation<WorkflowPublishHistory[]>;
}
