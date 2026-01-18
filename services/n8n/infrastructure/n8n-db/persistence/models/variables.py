"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/entities/variables.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/entities 的模块。导入/依赖:外部:无；内部:@n8n/typeorm；本地:./abstract-entity、./project。导出:Variables。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/entities/variables.ts -> services/n8n/infrastructure/n8n-db/persistence/models/variables.py

import { Column, Entity, ManyToOne } from '@n8n/typeorm';

import { WithStringId } from './abstract-entity';
import type { Project } from './project';

@Entity()
export class Variables extends WithStringId {
	@Column('text')
	key: string;

	@Column('text', { default: 'string' })
	type: string;

	@Column('text')
	value: string;

	// If null, it's a global variable
	@ManyToOne('Project', {
		onDelete: 'CASCADE',
		nullable: true,
	})
	project: Project | null;
}
