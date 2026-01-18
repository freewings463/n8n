"""
MIGRATION-META:
  source_path: packages/cli/src/public-api/v1/handlers/tags/tags.handler.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/public-api/v1/handlers 的模块。导入/依赖:外部:express；内部:@n8n/db、@n8n/di、@n8n/typeorm、@/services/tag.service；本地:../../types、../services/pagination.service。导出:无。关键函数/方法:apiKeyHasScopeWithGlobalScopeFallback、async。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/public-api/v1/handlers/tags/tags.handler.ts -> services/n8n/presentation/cli/api/public-api/v1/handlers/tags/tags_handler.py

import type { TagEntity } from '@n8n/db';
import { TagRepository } from '@n8n/db';
import { Container } from '@n8n/di';
// eslint-disable-next-line n8n-local-rules/misplaced-n8n-typeorm-import
import type { FindManyOptions } from '@n8n/typeorm';
import type express from 'express';

import { TagService } from '@/services/tag.service';

import type { TagRequest } from '../../../types';
import {
	apiKeyHasScopeWithGlobalScopeFallback,
	validCursor,
} from '../../shared/middlewares/global.middleware';
import { encodeNextCursor } from '../../shared/services/pagination.service';

export = {
	createTag: [
		apiKeyHasScopeWithGlobalScopeFallback({ scope: 'tag:create' }),
		async (req: TagRequest.Create, res: express.Response): Promise<express.Response> => {
			const { name } = req.body;

			const newTag = Container.get(TagService).toEntity({ name: name.trim() });

			try {
				const createdTag = await Container.get(TagService).save(newTag, 'create');
				return res.status(201).json(createdTag);
			} catch (error) {
				return res.status(409).json({ message: 'Tag already exists' });
			}
		},
	],
	updateTag: [
		apiKeyHasScopeWithGlobalScopeFallback({ scope: 'tag:update' }),
		async (req: TagRequest.Update, res: express.Response): Promise<express.Response> => {
			const { id } = req.params;
			const { name } = req.body;

			try {
				await Container.get(TagService).getById(id);
			} catch (error) {
				return res.status(404).json({ message: 'Not Found' });
			}

			const updateTag = Container.get(TagService).toEntity({ id, name: name.trim() });

			try {
				const updatedTag = await Container.get(TagService).save(updateTag, 'update');
				return res.json(updatedTag);
			} catch (error) {
				return res.status(409).json({ message: 'Tag already exists' });
			}
		},
	],
	deleteTag: [
		apiKeyHasScopeWithGlobalScopeFallback({ scope: 'tag:delete' }),
		async (req: TagRequest.Delete, res: express.Response): Promise<express.Response> => {
			const { id } = req.params;

			let tag;
			try {
				tag = await Container.get(TagService).getById(id);
			} catch (error) {
				return res.status(404).json({ message: 'Not Found' });
			}

			await Container.get(TagService).delete(id);
			return res.json(tag);
		},
	],
	getTags: [
		apiKeyHasScopeWithGlobalScopeFallback({ scope: 'tag:list' }),
		validCursor,
		async (req: TagRequest.GetAll, res: express.Response): Promise<express.Response> => {
			const { offset = 0, limit = 100 } = req.query;

			const query: FindManyOptions<TagEntity> = {
				skip: offset,
				take: limit,
			};

			const [tags, count] = await Container.get(TagRepository).findAndCount(query);

			return res.json({
				data: tags,
				nextCursor: encodeNextCursor({
					offset,
					limit,
					numberOfTotalRecords: count,
				}),
			});
		},
	],
	getTag: [
		apiKeyHasScopeWithGlobalScopeFallback({ scope: 'tag:read' }),
		async (req: TagRequest.Get, res: express.Response): Promise<express.Response> => {
			const { id } = req.params;

			try {
				const tag = await Container.get(TagService).getById(id);
				return res.json(tag);
			} catch (error) {
				return res.status(404).json({ message: 'Not Found' });
			}
		},
	],
};
