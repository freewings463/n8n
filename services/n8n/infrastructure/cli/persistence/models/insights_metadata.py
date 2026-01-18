"""
MIGRATION-META:
  source_path: packages/cli/src/modules/insights/database/entities/insights-metadata.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/modules/insights/database 的Insights模块。导入/依赖:外部:无；内部:@n8n/typeorm；本地:无。导出:InsightsMetadata。关键函数/方法:无。用于承载Insights实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/insights/database/entities/insights-metadata.ts -> services/n8n/infrastructure/cli/persistence/models/insights_metadata.py

import { BaseEntity, Column, Entity, PrimaryGeneratedColumn } from '@n8n/typeorm';

@Entity()
export class InsightsMetadata extends BaseEntity {
	@PrimaryGeneratedColumn()
	metaId: number;

	@Column({ unique: true, type: 'varchar', length: 36 })
	workflowId: string;

	@Column({ type: 'varchar', length: 36 })
	projectId: string;

	@Column({ type: 'varchar', length: 128 })
	workflowName: string;

	@Column({ type: 'varchar', length: 255 })
	projectName: string;
}
