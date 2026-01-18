"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/entities/workflow-dependency-entity.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/entities 的工作流模块。导入/依赖:外部:无；内部:无；本地:./abstract-entity、./workflow-entity。导出:DependencyType、WorkflowDependency。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/entities/workflow-dependency-entity.ts -> services/n8n/infrastructure/n8n-db/persistence/models/workflow_dependency_entity.py

import {
	Column,
	Entity,
	Index,
	JoinColumn,
	ManyToOne,
	PrimaryGeneratedColumn,
	Relation,
} from '@n8n/typeorm';

import { WithCreatedAt } from './abstract-entity';
import type { WorkflowEntity } from './workflow-entity';

export type DependencyType = 'credentialId' | 'nodeType' | 'webhookPath' | 'workflowCall';

@Entity({ name: 'workflow_dependency' })
export class WorkflowDependency extends WithCreatedAt {
	@PrimaryGeneratedColumn()
	id: number;

	/**
	 * The ID of the workflow the dependency belongs to.
	 */
	@Column({ length: 36 })
	@Index()
	workflowId: string;

	/**
	 * The version ID of the workflow the dependency belongs to.
	 * Used to ensure consistency between the workflow and dependency tables.
	 */
	@Column({ type: 'int' })
	workflowVersionId: number;

	/**
	 * The type of the dependency.
	 * credentialId | nodeType | webhookPath | workflowCall
	 */
	@Column({ length: 32 })
	@Index()
	dependencyType: DependencyType;

	/**
	 * The ID of the dependency, interpreted based on the dependency type.
	 * E.g., for 'credentialId' it would be the credential ID, for 'nodeType' the node type name, etc.
	 */
	@Column({ length: 255 })
	@Index()
	dependencyKey: string;

	/**
	 * Additional information about the dependency, interpreted based on the type.
	 * E.g., for 'nodeType' it could be the node ID, for 'webhookPath' the webhook ID.
	 */
	@Column({ type: 'json', nullable: true })
	dependencyInfo: Record<string, unknown> | null;

	/**
	 * The version of the index structure. Used for migrations and updates.
	 */
	@Column({ type: 'smallint', default: 1 })
	indexVersionId: number;

	@ManyToOne('WorkflowEntity', {
		onDelete: 'CASCADE',
	})
	@JoinColumn({ name: 'workflowId' })
	workflow: Relation<WorkflowEntity>;
}
