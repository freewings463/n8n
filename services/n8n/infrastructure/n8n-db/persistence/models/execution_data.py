"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/entities/execution-data.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/entities 的执行模块。导入/依赖:外部:无；内部:@n8n/typeorm、n8n-workflow；本地:./abstract-entity、./execution-entity、./types-db、../utils/transformers。导出:ExecutionData。关键函数/方法:无。用于承载执行实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/entities/execution-data.ts -> services/n8n/infrastructure/n8n-db/persistence/models/execution_data.py

import { Column, Entity, JoinColumn, OneToOne, PrimaryColumn } from '@n8n/typeorm';
import { IWorkflowBase } from 'n8n-workflow';

import { JsonColumn } from './abstract-entity';
import { ExecutionEntity } from './execution-entity';
import { ISimplifiedPinData } from './types-db';
import { idStringifier } from '../utils/transformers';

@Entity()
export class ExecutionData {
	@Column('text')
	data: string;

	// WARNING: the workflowData column has been changed from IWorkflowDb to IWorkflowBase
	// when ExecutionData was introduced as a separate entity.
	// This is because manual executions of unsaved workflows have no workflow id
	// and IWorkflowDb has it as a mandatory field. IWorkflowBase reflects the correct
	// data structure for this entity.
	/**
	 * Workaround: Pindata causes TS errors from excessively deep type instantiation
	 * due to `INodeExecutionData`, so we use a simplified version so `QueryDeepPartialEntity`
	 * can resolve and calls to `update`, `insert`, and `insert` pass typechecking.
	 */
	@JsonColumn()
	workflowData: Omit<IWorkflowBase, 'pinData'> & { pinData?: ISimplifiedPinData };

	@PrimaryColumn({ transformer: idStringifier })
	executionId: string;

	@Column({ type: 'varchar', length: 36, nullable: true })
	workflowVersionId: string | null;

	@OneToOne('ExecutionEntity', 'executionData', {
		onDelete: 'CASCADE',
	})
	@JoinColumn({
		name: 'executionId',
	})
	execution: ExecutionEntity;
}
