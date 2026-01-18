"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/entities/binary-data-file.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/entities 的模块。导入/依赖:外部:zod；内部:@n8n/typeorm；本地:./abstract-entity。导出:SourceTypeSchema、SourceType、BinaryDataFile。关键函数/方法:Index。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/entities/binary-data-file.ts -> services/n8n/infrastructure/n8n-db/persistence/models/binary_data_file.py

import { Column, Entity, Index, PrimaryColumn } from '@n8n/typeorm';
import { z } from 'zod';

import { BinaryColumn, WithTimestamps } from './abstract-entity';

export const SourceTypeSchema = z.enum(['execution', 'chat_message_attachment']);

export type SourceType = z.infer<typeof SourceTypeSchema>;

@Entity('binary_data')
export class BinaryDataFile extends WithTimestamps {
	@PrimaryColumn('uuid')
	fileId: string;

	@Column('varchar', { length: 50 })
	sourceType: SourceType;

	@Column('varchar', { length: 255 })
	sourceId: string;

	@BinaryColumn()
	data: Buffer;

	@Column('varchar', { length: 255, nullable: true })
	mimeType: string | null;

	@Column('varchar', { length: 255, nullable: true })
	fileName: string | null;

	@Column('int')
	fileSize: number; // bytes
}

Index(['sourceType', 'sourceId'])(BinaryDataFile);
