"""
MIGRATION-META:
  source_path: packages/cli/src/controllers/annotation-tags.controller.ee.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/controllers 的控制器。导入/依赖:外部:无；内部:@n8n/decorators、@/requests、@/services/annotation-tag.service.ee；本地:无。导出:AnnotationTagsController。关键函数/方法:getAll、createTag、updateTag、deleteTag。用于处理该模块接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected @RestController/@Controller from @n8n/decorators
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/controllers/annotation-tags.controller.ee.ts -> services/n8n/presentation/cli/api/v1/controllers/annotation_tags_controller_ee.py

import { Delete, Get, Patch, Post, RestController, GlobalScope } from '@n8n/decorators';

import { AnnotationTagsRequest } from '@/requests';
import { AnnotationTagService } from '@/services/annotation-tag.service.ee';

@RestController('/annotation-tags')
export class AnnotationTagsController {
	constructor(private readonly annotationTagService: AnnotationTagService) {}

	@Get('/')
	@GlobalScope('annotationTag:list')
	async getAll(req: AnnotationTagsRequest.GetAll) {
		return await this.annotationTagService.getAll({
			withUsageCount: req.query.withUsageCount === 'true',
		});
	}

	@Post('/')
	@GlobalScope('annotationTag:create')
	async createTag(req: AnnotationTagsRequest.Create) {
		const tag = this.annotationTagService.toEntity({ name: req.body.name });

		return await this.annotationTagService.save(tag);
	}

	@Patch('/:id')
	@GlobalScope('annotationTag:update')
	async updateTag(req: AnnotationTagsRequest.Update) {
		const newTag = this.annotationTagService.toEntity({
			id: req.params.id,
			name: req.body.name.trim(),
		});

		return await this.annotationTagService.save(newTag);
	}

	@Delete('/:id')
	@GlobalScope('annotationTag:delete')
	async deleteTag(req: AnnotationTagsRequest.Delete) {
		const { id } = req.params;

		await this.annotationTagService.delete(id);

		return true;
	}
}
