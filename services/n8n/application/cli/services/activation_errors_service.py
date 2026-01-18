"""
MIGRATION-META:
  source_path: packages/cli/src/activation-errors.service.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src 的服务。导入/依赖:外部:无；内部:@n8n/di、@/services/…/cache.service；本地:无。导出:ActivationErrorsService。关键函数/方法:register、get、deregister、getAll、clearAll。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/activation-errors.service.ts -> services/n8n/application/cli/services/activation_errors_service.py

import { Service } from '@n8n/di';

import { CacheService } from '@/services/cache/cache.service';

@Service()
export class ActivationErrorsService {
	private readonly cacheKey = 'workflow-activation-errors';

	constructor(private readonly cacheService: CacheService) {}

	async register(workflowId: string, errorMessage: string) {
		await this.cacheService.setHash(this.cacheKey, { [workflowId]: errorMessage });
	}

	async deregister(workflowId: string) {
		await this.cacheService.deleteFromHash(this.cacheKey, workflowId);
	}

	async get(workflowId: string) {
		const activationError = await this.cacheService.getHashValue<string>(this.cacheKey, workflowId);

		if (!activationError) return null;

		return activationError;
	}

	async getAll() {
		const activationErrors = await this.cacheService.getHash<string>(this.cacheKey);

		if (!activationErrors) return {};

		return activationErrors;
	}

	async clearAll() {
		await this.cacheService.delete(this.cacheKey);
	}
}
