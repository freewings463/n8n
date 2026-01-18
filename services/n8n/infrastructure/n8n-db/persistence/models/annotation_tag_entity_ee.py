"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/entities/annotation-tag-entity.ee.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/entities 的模块。导入/依赖:外部:class-validator；内部:@n8n/typeorm；本地:./abstract-entity、./annotation-tag-mapping.ee、./execution-annotation.ee。导出:AnnotationTagEntity。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/entities/annotation-tag-entity.ee.ts -> services/n8n/infrastructure/n8n-db/persistence/models/annotation_tag_entity_ee.py

import { Column, Entity, Index, ManyToMany, OneToMany } from '@n8n/typeorm';
import { IsString, Length } from 'class-validator';

import { WithTimestampsAndStringId } from './abstract-entity';
import type { AnnotationTagMapping } from './annotation-tag-mapping.ee';
import type { ExecutionAnnotation } from './execution-annotation.ee';

@Entity()
export class AnnotationTagEntity extends WithTimestampsAndStringId {
	@Column({ length: 24 })
	@Index({ unique: true })
	@IsString({ message: 'Tag name must be of type string.' })
	@Length(1, 24, { message: 'Tag name must be $constraint1 to $constraint2 characters long.' })
	name: string;

	@ManyToMany('ExecutionAnnotation', 'tags')
	annotations: ExecutionAnnotation[];

	@OneToMany('AnnotationTagMapping', 'tags')
	annotationMappings: AnnotationTagMapping[];
}
