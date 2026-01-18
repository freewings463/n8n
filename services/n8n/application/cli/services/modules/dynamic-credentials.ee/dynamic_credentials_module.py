"""
MIGRATION-META:
  source_path: packages/cli/src/modules/dynamic-credentials.ee/dynamic-credentials.module.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/dynamic-credentials.ee 的模块。导入/依赖:外部:无；内部:@n8n/constants、@n8n/decorators、@n8n/di；本地:./dynamic-credentials.controller、./credential-resolvers.controller、./context-establishment-hooks、./credential-resolvers 等5项。导出:DynamicCredentialsModule。关键函数/方法:init、isFeatureFlagEnabled、entities、shutdown。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/dynamic-credentials.ee/dynamic-credentials.module.ts -> services/n8n/application/cli/services/modules/dynamic-credentials.ee/dynamic_credentials_module.py

import { LICENSE_FEATURES } from '@n8n/constants';
import type { ModuleInterface } from '@n8n/decorators';
import { BackendModule, OnShutdown } from '@n8n/decorators';
import { Container } from '@n8n/di';

function isFeatureFlagEnabled(): boolean {
	return process.env.N8N_ENV_FEAT_DYNAMIC_CREDENTIALS === 'true';
}

@BackendModule({ name: 'dynamic-credentials', licenseFlag: LICENSE_FEATURES.DYNAMIC_CREDENTIALS })
export class DynamicCredentialsModule implements ModuleInterface {
	async init() {
		if (!isFeatureFlagEnabled()) {
			return;
		}
		await import('./dynamic-credentials.controller');
		await import('./credential-resolvers.controller');
		await import('./context-establishment-hooks');
		await import('./credential-resolvers');
		const {
			DynamicCredentialResolverRegistry,
			DynamicCredentialStorageService,
			DynamicCredentialService,
		} = await import('./services');
		await import('./workflow-status.controller');

		await Container.get(DynamicCredentialResolverRegistry).init();

		// Register the credential resolution provider with CredentialsHelper
		const { DynamicCredentialsProxy } = await import('../../credentials/dynamic-credentials-proxy');
		const credentialsProxy = Container.get(DynamicCredentialsProxy);
		const dynamicCredentialService = Container.get(DynamicCredentialService);
		const dynamicCredentialStorageService = Container.get(DynamicCredentialStorageService);
		credentialsProxy.setResolverProvider(dynamicCredentialService);
		credentialsProxy.setStorageProvider(dynamicCredentialStorageService);
	}

	async entities() {
		if (!isFeatureFlagEnabled()) {
			return [];
		}
		const { DynamicCredentialResolver } = await import('./database/entities/credential-resolver');
		const { DynamicCredentialEntry } = await import('./database/entities/dynamic-credential-entry');

		return [DynamicCredentialResolver, DynamicCredentialEntry];
	}

	@OnShutdown()
	async shutdown() {}
}
