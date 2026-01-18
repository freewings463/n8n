"""
MIGRATION-META:
  source_path: packages/cli/src/modules/external-secrets.ee/provider-registry.service.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/external-secrets.ee 的服务。导入/依赖:外部:无；内部:@n8n/di；本地:./types。导出:ExternalSecretsProviderRegistry。关键函数/方法:get、add、remove、has、getAll、getConnected、getNames、clear、disconnectAll、async。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/external-secrets.ee/provider-registry.service.ts -> services/n8n/application/cli/services/external-secrets.ee/provider_registry_service.py

import { Service } from '@n8n/di';

import type { SecretsProvider } from './types';

/**
 * Manages the collection of active secrets providers
 * Provides simple CRUD operations for providers
 */
@Service()
export class ExternalSecretsProviderRegistry {
	private providers = new Map<string, SecretsProvider>();

	add(name: string, provider: SecretsProvider): void {
		this.providers.set(name, provider);
	}

	remove(name: string): void {
		this.providers.delete(name);
	}

	get(name: string): SecretsProvider | undefined {
		return this.providers.get(name);
	}

	has(name: string): boolean {
		return this.providers.has(name);
	}

	getAll(): Map<string, SecretsProvider> {
		return new Map(this.providers);
	}

	getConnected(): SecretsProvider[] {
		return Array.from(this.providers.values()).filter((p) => p.state === 'connected');
	}

	getNames(): string[] {
		return Array.from(this.providers.keys());
	}

	clear(): void {
		this.providers.clear();
	}

	async disconnectAll(): Promise<void> {
		const disconnectPromises = Array.from(this.providers.values()).map(
			async (provider) =>
				await provider.disconnect().catch(() => {
					// Ignore errors during shutdown
				}),
		);
		await Promise.all(disconnectPromises);
	}
}
