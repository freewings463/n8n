"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/entities/workflow-statistics.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/entities 的工作流模块。导入/依赖:外部:无；内部:@n8n/typeorm；本地:./abstract-entity、./types-db、./workflow-entity。导出:WorkflowStatistics。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/entities/workflow-statistics.ts -> services/n8n/infrastructure/n8n-db/persistence/models/workflow_statistics.py

import { Column, Entity, ManyToOne, PrimaryColumn } from '@n8n/typeorm';

import { DateTimeColumn } from './abstract-entity';
import { StatisticsNames } from './types-db';
import { WorkflowEntity } from './workflow-entity';

@Entity()
export class WorkflowStatistics {
	@Column()
	count: number;

	@Column()
	rootCount: number;

	@DateTimeColumn()
	latestEvent: Date;

	@PrimaryColumn({ length: 128 })
	name: StatisticsNames;

	@ManyToOne('WorkflowEntity', 'shared')
	workflow: WorkflowEntity;

	@PrimaryColumn()
	workflowId: string;
}
