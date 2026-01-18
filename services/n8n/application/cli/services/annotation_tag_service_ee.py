"""
MIGRATION-META:
  source_path: packages/cli/src/services/annotation-tag.service.ee.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/services 的服务。导入/依赖:外部:无；内部:@n8n/db、@n8n/di、@/generic-helpers；本地:无。导出:AnnotationTagService。关键函数/方法:save、delete、toEntity、allTags。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/services/annotation-tag.service.ee.ts -> services/n8n/application/cli/services/annotation_tag_service_ee.py

import type { AnnotationTagEntity } from '@n8n/db';
import { AnnotationTagRepository } from '@n8n/db';
import { Service } from '@n8n/di';

import { validateEntity } from '@/generic-helpers';

type IAnnotationTagDb = Pick<AnnotationTagEntity, 'id' | 'name' | 'createdAt' | 'updatedAt'>;

type IAnnotationTagWithCountDb = IAnnotationTagDb & { usageCount: number };

type GetAllResult<T> = T extends { withUsageCount: true }
	? IAnnotationTagWithCountDb[]
	: IAnnotationTagDb[];

@Service()
export class AnnotationTagService {
	constructor(private tagRepository: AnnotationTagRepository) {}

	toEntity(attrs: { name: string; id?: string }) {
		attrs.name = attrs.name.trim();

		return this.tagRepository.create(attrs);
	}

	async save(tag: AnnotationTagEntity) {
		await validateEntity(tag);

		return await this.tagRepository.save(tag, { transaction: false });
	}

	async delete(id: string) {
		return await this.tagRepository.delete(id);
	}

	async getAll<T extends { withUsageCount: boolean }>(options?: T): Promise<GetAllResult<T>> {
		if (options?.withUsageCount) {
			const allTags = await this.tagRepository.find({
				select: ['id', 'name', 'createdAt', 'updatedAt'],
				relations: ['annotationMappings'],
			});

			return allTags.map(({ annotationMappings, ...rest }) => {
				return {
					...rest,
					usageCount: annotationMappings.length,
				} as IAnnotationTagWithCountDb;
			}) as GetAllResult<T>;
		}

		const allTags = (await this.tagRepository.find({
			select: ['id', 'name', 'createdAt', 'updatedAt'],
		})) as IAnnotationTagDb[];

		return allTags as GetAllResult<T>;
	}
}
