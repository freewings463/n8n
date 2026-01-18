"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/entities/processed-data.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/entities 的模块。导入/依赖:外部:无；内部:@n8n/typeorm、n8n-workflow；本地:./abstract-entity、../utils/transformers。导出:ProcessedData。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/entities/processed-data.ts -> services/n8n/infrastructure/n8n-db/persistence/models/processed_data.py

import { Entity, PrimaryColumn } from '@n8n/typeorm';
import type { IProcessedDataEntries, IProcessedDataLatest } from 'n8n-workflow';

import { JsonColumn, WithTimestamps } from './abstract-entity';
import { objectRetriever } from '../utils/transformers';

@Entity()
export class ProcessedData extends WithTimestamps {
	@PrimaryColumn('varchar')
	context: string;

	@PrimaryColumn()
	workflowId: string;

	@JsonColumn({
		nullable: true,
		transformer: objectRetriever,
	})
	value: IProcessedDataEntries | IProcessedDataLatest;
}
