"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/entities/execution-metadata.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/entities 的执行模块。导入/依赖:外部:无；内部:@n8n/typeorm；本地:./execution-entity。导出:ExecutionMetadata。关键函数/方法:无。用于承载执行实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/entities/execution-metadata.ts -> services/n8n/infrastructure/n8n-db/persistence/models/execution_metadata.py

import { Column, Entity, ManyToOne, PrimaryGeneratedColumn } from '@n8n/typeorm';

import { ExecutionEntity } from './execution-entity';

@Entity()
export class ExecutionMetadata {
	@PrimaryGeneratedColumn()
	id: number;

	@ManyToOne('ExecutionEntity', 'metadata', {
		onDelete: 'CASCADE',
	})
	execution: ExecutionEntity;

	@Column()
	executionId: string;

	@Column('text')
	key: string;

	@Column('text')
	value: string;
}
