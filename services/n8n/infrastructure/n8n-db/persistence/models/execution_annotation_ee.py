"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/entities/execution-annotation.ee.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/entities 的执行模块。导入/依赖:外部:无；内部:n8n-workflow；本地:./annotation-tag-entity.ee、./annotation-tag-mapping.ee、./execution-entity。导出:ExecutionAnnotation。关键函数/方法:无。用于承载执行实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/entities/execution-annotation.ee.ts -> services/n8n/infrastructure/n8n-db/persistence/models/execution_annotation_ee.py

import {
	Column,
	Entity,
	Index,
	JoinColumn,
	JoinTable,
	ManyToMany,
	OneToMany,
	OneToOne,
	PrimaryGeneratedColumn,
	RelationId,
} from '@n8n/typeorm';
import type { AnnotationVote } from 'n8n-workflow';

import type { AnnotationTagEntity } from './annotation-tag-entity.ee';
import type { AnnotationTagMapping } from './annotation-tag-mapping.ee';
import { ExecutionEntity } from './execution-entity';

@Entity({ name: 'execution_annotations' })
export class ExecutionAnnotation {
	@PrimaryGeneratedColumn()
	id: number;

	/**
	 * This field stores the up- or down-vote of the execution by user.
	 */
	@Column({ type: 'varchar', nullable: true })
	vote: AnnotationVote | null;

	/**
	 * Custom text note added to the execution by user.
	 */
	@Column({ type: 'varchar', nullable: true })
	note: string | null;

	@RelationId((annotation: ExecutionAnnotation) => annotation.execution)
	executionId: string;

	@Index({ unique: true })
	@OneToOne('ExecutionEntity', 'annotation', {
		onDelete: 'CASCADE',
	})
	@JoinColumn({ name: 'executionId' })
	execution: ExecutionEntity;

	@ManyToMany('AnnotationTagEntity', 'annotations')
	@JoinTable({
		name: 'execution_annotation_tags', // table name for the junction table of this relation
		joinColumn: {
			name: 'annotationId',
			referencedColumnName: 'id',
		},
		inverseJoinColumn: {
			name: 'tagId',
			referencedColumnName: 'id',
		},
	})
	tags?: AnnotationTagEntity[];

	@OneToMany('AnnotationTagMapping', 'annotations')
	tagMappings: AnnotationTagMapping[];
}
