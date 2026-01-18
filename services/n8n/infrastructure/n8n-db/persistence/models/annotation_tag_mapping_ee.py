"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/entities/annotation-tag-mapping.ee.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/entities 的模块。导入/依赖:外部:无；内部:@n8n/typeorm；本地:./annotation-tag-entity.ee、./execution-annotation.ee。导出:AnnotationTagMapping。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/entities/annotation-tag-mapping.ee.ts -> services/n8n/infrastructure/n8n-db/persistence/models/annotation_tag_mapping_ee.py

import { Entity, JoinColumn, ManyToOne, PrimaryColumn } from '@n8n/typeorm';

import type { AnnotationTagEntity } from './annotation-tag-entity.ee';
import type { ExecutionAnnotation } from './execution-annotation.ee';

/**
 * This entity represents the junction table between the execution annotations and the tags
 */
@Entity({ name: 'execution_annotation_tags' })
export class AnnotationTagMapping {
	@PrimaryColumn()
	annotationId: number;

	@ManyToOne('ExecutionAnnotation', 'tagMappings')
	@JoinColumn({ name: 'annotationId' })
	annotations: ExecutionAnnotation[];

	@PrimaryColumn()
	tagId: string;

	@ManyToOne('AnnotationTagEntity', 'annotationMappings')
	@JoinColumn({ name: 'tagId' })
	tags: AnnotationTagEntity[];
}
