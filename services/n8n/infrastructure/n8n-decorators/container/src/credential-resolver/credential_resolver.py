"""
MIGRATION-META:
  source_path: packages/@n8n/decorators/src/credential-resolver/credential-resolver.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/decorators/src/credential-resolver 的模块。导入/依赖:外部:无；内部:@n8n/di；本地:无。导出:CredentialResolverConfiguration、CredentialResolverHandle、CredentialResolverMetadata、ICredentialResolver、CredentialResolverClass。关键函数/方法:getSecret、setSecret、validateOptions。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - DI/container wiring -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/decorators/src/credential-resolver/credential-resolver.ts -> services/n8n/infrastructure/n8n-decorators/container/src/credential-resolver/credential_resolver.py

import type { Constructable } from '@n8n/di';
import type {
	ICredentialContext,
	ICredentialDataDecryptedObject,
	INodeProperties,
} from 'n8n-workflow';

/**
 * Configuration object passed to resolver methods. Structure is defined by resolver type's metadata.options.
 */
export type CredentialResolverConfiguration = Record<string, unknown>;

export type CredentialResolverHandle = {
	configuration: CredentialResolverConfiguration;
	resolverName: string;
	resolverId: string;
};

/**
 * Metadata describing a credential resolver type for UI integration and discovery.
 */
export interface CredentialResolverMetadata {
	/** Unique identifier for the resolver type */
	name: string;

	/** Human-readable description of what this resolver does */
	description: string;

	/** Optional display name shown in UI. Falls back to name if not provided. */
	displayName?: string;

	/** Configuration schema using n8n's INodeProperties format for dynamic form rendering */
	options?: INodeProperties[];
}

/**
 * Core interface for credential resolver implementations.
 * Resolvers fetch credential data dynamically based on execution context and configuration.
 */
export interface ICredentialResolver {
	/** Metadata for UI integration and resolver discovery */
	metadata: CredentialResolverMetadata;

	/**
	 * Retrieves credential data for a specific entity from the resolver's storage.
	 * @throws {CredentialResolverDataNotFoundError} When no data exists for the given context
	 * @throws {CredentialResolverError} For other resolver-specific errors
	 */
	getSecret(
		credentialId: string,
		context: ICredentialContext,
		handle: CredentialResolverHandle,
	): Promise<ICredentialDataDecryptedObject>;

	/**
	 * Stores credential data for a specific entity in the resolver's storage.
	 * @throws {CredentialResolverError} When storage operation fails
	 */
	setSecret(
		credentialId: string,
		context: ICredentialContext,
		data: ICredentialDataDecryptedObject,
		handle: CredentialResolverHandle,
	): Promise<void>;

	/**
	 * Deletes credential data for a specific entity from the resolver's storage.
	 * Optional - not all resolvers support deletion.
	 * @throws {CredentialResolverError} When deletion operation fails
	 */
	deleteSecret?(
		credentialId: string,
		context: ICredentialContext,
		handle: CredentialResolverHandle,
	): Promise<void>;

	/**
	 * Deletes all credential data for the resolver.
	 * Optional - not all resolvers support deletion.
	 * @throws {CredentialResolverError} When deletion operation fails
	 */
	deleteAllSecrets?(handle: CredentialResolverHandle): Promise<void>;

	/**
	 * Validates resolver configuration before saving.
	 * Should verify connectivity, authentication, and configuration structure.
	 * @throws {CredentialResolverValidationError} When configuration is invalid
	 */
	validateOptions(options: CredentialResolverConfiguration): Promise<void>;

	/**
	 * Validates if the userIdentity provided has access to the resolver capable credential
	 *
	 * @param identity - The identity of the entity to validate access for
	 * @throws {CredentialResolverAccessValidationError} When access is invalid
	 */
	validateIdentity?(identity: string, handle: CredentialResolverHandle): Promise<void>;

	/**
	 * Runs initialization logic for the resolver. This might be called multiple times!
	 * Optional - not all resolvers require initialization.
	 */
	init?(): Promise<void>;
}

/**
 * Type helper for credential resolver class constructors.
 */
export type CredentialResolverClass = Constructable<ICredentialResolver>;
