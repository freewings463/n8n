"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/repositories/folder-tag-mapping.repository.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/repositories 的仓储。导入/依赖:外部:无；内部:@n8n/di、@n8n/typeorm；本地:../entities/folder-tag-mapping。导出:FolderTagMappingRepository。关键函数/方法:overwriteTags。用于封装该模块数据读写与查询细节，隔离持久层。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected TypeORM Repository/EntityManager usage
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/repositories/folder-tag-mapping.repository.ts -> services/n8n/infrastructure/n8n-db/persistence/repositories/folder_tag_mapping_repository.py

import { Service } from '@n8n/di';
import { DataSource, Repository } from '@n8n/typeorm';

import { FolderTagMapping } from '../entities/folder-tag-mapping';

@Service()
export class FolderTagMappingRepository extends Repository<FolderTagMapping> {
	constructor(dataSource: DataSource) {
		super(FolderTagMapping, dataSource.manager);
	}

	async overwriteTags(folderId: string, tagIds: string[]) {
		return await this.manager.transaction(async (tx) => {
			await tx.delete(FolderTagMapping, { folderId });

			const tags = tagIds.map((tagId) => this.create({ folderId, tagId }));

			return await tx.insert(FolderTagMapping, tags);
		});
	}
}
