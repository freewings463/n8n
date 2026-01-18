"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/repositories/tag.repository.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/repositories 的仓储。导入/依赖:外部:lodash/intersection；内部:@n8n/di、@n8n/typeorm；本地:../entities、../entities/types-db。导出:TagRepository。关键函数/方法:findMany、setTags、getWorkflowIdsViaTags。用于封装该模块数据读写与查询细节，隔离持久层。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected TypeORM Repository/EntityManager usage
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/repositories/tag.repository.ts -> services/n8n/infrastructure/n8n-db/persistence/repositories/tag_repository.py

import { Service } from '@n8n/di';
import type { EntityManager } from '@n8n/typeorm';
import { DataSource, In, Repository } from '@n8n/typeorm';
import intersection from 'lodash/intersection';

import { TagEntity } from '../entities';
import type { IWorkflowDb } from '../entities/types-db';

@Service()
export class TagRepository extends Repository<TagEntity> {
	constructor(dataSource: DataSource) {
		super(TagEntity, dataSource.manager);
	}

	async findMany(tagIds: string[]) {
		return await this.find({
			select: ['id', 'name'],
			where: { id: In(tagIds) },
		});
	}

	/**
	 * Set tags on workflow to import while ensuring all tags exist in the database,
	 * either by matching incoming to existing tags or by creating them first.
	 */
	async setTags(tx: EntityManager, dbTags: TagEntity[], workflow: IWorkflowDb) {
		if (!workflow?.tags?.length) return;

		for (let i = 0; i < workflow.tags.length; i++) {
			const importTag = workflow.tags[i];

			if (!importTag.name) continue;

			const identicalMatch = dbTags.find(
				(dbTag) =>
					dbTag.id === importTag.id &&
					dbTag.createdAt &&
					importTag.createdAt &&
					dbTag.createdAt.getTime() === new Date(importTag.createdAt).getTime(),
			);

			if (identicalMatch) {
				workflow.tags[i] = identicalMatch;
				continue;
			}

			const nameMatch = dbTags.find((dbTag) => dbTag.name === importTag.name);

			if (nameMatch) {
				workflow.tags[i] = nameMatch;
				continue;
			}

			const tagEntity = this.create(importTag);

			workflow.tags[i] = await tx.save<TagEntity>(tagEntity);
		}
	}

	/**
	 * Returns the workflow IDs that have certain tags.
	 * Intersection! e.g. workflow needs to have all provided tags.
	 */
	async getWorkflowIdsViaTags(tags: string[]): Promise<string[]> {
		const dbTags = await this.find({
			where: { name: In(tags) },
			relations: ['workflows'],
			select: {
				id: true,
				workflows: {
					id: true,
				},
			},
		});

		const workflowIdsPerTag = dbTags.map((tag) => tag.workflows.map((workflow) => workflow.id));

		return intersection(...workflowIdsPerTag);
	}
}
