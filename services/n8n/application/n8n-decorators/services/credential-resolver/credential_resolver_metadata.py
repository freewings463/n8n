"""
MIGRATION-META:
  source_path: packages/@n8n/decorators/src/credential-resolver/credential-resolver-metadata.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/decorators/src/credential-resolver 的模块。导入/依赖:外部:无；内部:@n8n/di；本地:./credential-resolver。导出:CredentialResolverEntryMetadata、CredentialResolver。关键函数/方法:register、getEntries、getClasses。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/decorators/src/credential-resolver/credential-resolver-metadata.ts -> services/n8n/application/n8n-decorators/services/credential-resolver/credential_resolver_metadata.py

import { Container, Service } from '@n8n/di';

import { CredentialResolverClass } from './credential-resolver';

type CredentialResolverEntry = {
	class: CredentialResolverClass;
};

/**
 * Registry service for credential resolver type discovery and instantiation.
 * Resolver classes decorated with @CredentialResolver() are automatically registered.
 */
@Service()
export class CredentialResolverEntryMetadata {
	private readonly credentialResolverEntries: Set<CredentialResolverEntry> = new Set();

	/** Registers a credential resolver class. Called automatically by @CredentialResolver() decorator. */
	register(credentialResolverEntry: CredentialResolverEntry) {
		this.credentialResolverEntries.add(credentialResolverEntry);
	}

	/** Returns all registered resolver entries as [index, entry] tuples. */
	getEntries() {
		return [...this.credentialResolverEntries.entries()];
	}

	/** Returns all registered resolver classes. */
	getClasses() {
		return [...this.credentialResolverEntries.values()].map((entry) => entry.class);
	}
}

/**
 * Decorator to mark a class as a credential resolver.
 * Automatically registers the resolver for discovery and enables dependency injection.
 *
 * @example
 * @CredentialResolver()
 * class MyResolver implements ICredentialResolver { ... }
 */
export const CredentialResolver =
	<T extends CredentialResolverClass>() =>
	(target: T) => {
		// Register resolver class for discovery by registry
		Container.get(CredentialResolverEntryMetadata).register({
			class: target,
		});

		// Enable dependency injection for the resolver class
		// eslint-disable-next-line @typescript-eslint/no-unsafe-return
		return Service()(target);
	};
