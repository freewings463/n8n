"""
MIGRATION-META:
  source_path: packages/cli/src/modules/external-secrets.ee/external-secrets.module.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/external-secrets.ee 的模块。导入/依赖:外部:无；内部:@n8n/decorators、@n8n/di、n8n-core；本地:./external-secrets.controller.ee、./external-secrets-manager.ee。导出:ExternalSecretsModule。关键函数/方法:init、shutdown。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/external-secrets.ee/external-secrets.module.ts -> services/n8n/application/cli/services/modules/external-secrets.ee/external_secrets_module.py

import type { ModuleInterface } from '@n8n/decorators';
import { BackendModule, OnShutdown } from '@n8n/decorators';
import { Container } from '@n8n/di';

@BackendModule({ name: 'external-secrets', licenseFlag: 'feat:externalSecrets' })
export class ExternalSecretsModule implements ModuleInterface {
	async init() {
		await import('./external-secrets.controller.ee');

		const { ExternalSecretsManager } = await import('./external-secrets-manager.ee');
		const { ExternalSecretsProxy } = await import('n8n-core');

		const externalSecretsManager = Container.get(ExternalSecretsManager);
		const externalSecretsProxy = Container.get(ExternalSecretsProxy);

		await externalSecretsManager.init();
		externalSecretsProxy.setManager(externalSecretsManager);
	}

	@OnShutdown()
	async shutdown() {
		const { ExternalSecretsManager } = await import('./external-secrets-manager.ee');

		Container.get(ExternalSecretsManager).shutdown();
	}
}
