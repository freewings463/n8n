"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/entities/workflow-tag-mapping.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/entities 的工作流模块。导入/依赖:外部:无；内部:@n8n/typeorm；本地:./tag-entity、./workflow-entity。导出:WorkflowTagMapping。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/entities/workflow-tag-mapping.ts -> services/n8n/infrastructure/n8n-db/persistence/models/workflow_tag_mapping.py

import { Entity, JoinColumn, ManyToOne, PrimaryColumn } from '@n8n/typeorm';

import type { TagEntity } from './tag-entity';
import type { WorkflowEntity } from './workflow-entity';

@Entity({ name: 'workflows_tags' })
export class WorkflowTagMapping {
	@PrimaryColumn()
	workflowId: string;

	@ManyToOne('WorkflowEntity', 'tagMappings')
	@JoinColumn({ name: 'workflowId' })
	workflows: WorkflowEntity[];

	@PrimaryColumn()
	tagId: string;

	@ManyToOne('TagEntity', 'workflowMappings')
	@JoinColumn({ name: 'tagId' })
	tags: TagEntity[];
}
