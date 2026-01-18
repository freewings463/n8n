"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/entities/folder-tag-mapping.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/entities 的模块。导入/依赖:外部:无；内部:@n8n/typeorm；本地:./folder、./tag-entity。导出:FolderTagMapping。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/entities/folder-tag-mapping.ts -> services/n8n/infrastructure/n8n-db/persistence/models/folder_tag_mapping.py

import { Entity, JoinColumn, ManyToOne, PrimaryColumn } from '@n8n/typeorm';

import type { Folder } from './folder';
import type { TagEntity } from './tag-entity';

@Entity({ name: 'folder_tag' })
export class FolderTagMapping {
	@PrimaryColumn()
	folderId: string;

	@ManyToOne('Folder', 'tagMappings')
	@JoinColumn({ name: 'folderId' })
	folders: Folder[];

	@PrimaryColumn()
	tagId: string;

	@ManyToOne('TagEntity', 'folderMappings')
	@JoinColumn({ name: 'tagId' })
	tags: TagEntity[];
}
