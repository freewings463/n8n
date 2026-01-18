"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/entities/workflow-publish-history.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/entities 的工作流模块。导入/依赖:外部:无；内部:无；本地:./abstract-entity、./user、./workflow-history。导出:WorkflowPublishHistory。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/entities/workflow-publish-history.ts -> services/n8n/infrastructure/n8n-db/persistence/models/workflow_publish_history.py

import {
	Column,
	Entity,
	Index,
	JoinColumn,
	ManyToOne,
	OneToOne,
	PrimaryGeneratedColumn,
	Relation,
} from '@n8n/typeorm';

import { WithCreatedAt } from './abstract-entity';
import { User } from './user';
import type { WorkflowHistory } from './workflow-history';

@Entity()
@Index(['workflowId', 'versionId'])
export class WorkflowPublishHistory extends WithCreatedAt {
	@PrimaryGeneratedColumn()
	id: number;

	@Column({ type: 'varchar' })
	workflowId: string;

	@Column({ type: 'varchar' })
	versionId: string;

	// Note that we only track "permanent" deactivations
	// We don't explicitly track the deactivations of a previous active version
	// which happens when a new active version of an already active workflow is published
	@Column()
	event: 'activated' | 'deactivated';

	@Column({ type: 'uuid', nullable: true })
	userId: string | null;

	@OneToOne('User', {
		onDelete: 'SET NULL',
		nullable: true,
	})
	@JoinColumn({ name: 'userId' })
	user: User | null;

	@ManyToOne('WorkflowHistory', 'workflowPublishHistory', { nullable: true })
	@JoinColumn({
		name: 'versionId',
	})
	workflowHistory: Relation<WorkflowHistory> | null;
}
