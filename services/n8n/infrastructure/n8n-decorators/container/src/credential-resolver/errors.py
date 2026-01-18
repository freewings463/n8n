"""
MIGRATION-META:
  source_path: packages/@n8n/decorators/src/credential-resolver/errors.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/decorators/src/credential-resolver 的模块。导入/依赖:外部:无；内部:无；本地:无。导出:CredentialResolverError、CredentialResolverDataNotFoundError、CredentialResolverValidationError。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。注释目标:Base error class for all credential resolver errors.。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - DI/container wiring -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/decorators/src/credential-resolver/errors.ts -> services/n8n/infrastructure/n8n-decorators/container/src/credential-resolver/errors.py

/**
 * Base error class for all credential resolver errors.
 */
export class CredentialResolverError extends Error {
	constructor(message: string) {
		super(message);
		this.name = 'CredentialResolverError';
	}
}

/**
 * Thrown when no credential data exists for the requested credential and context combination.
 * Indicates the entity has not stored credentials for this credential type.
 */
export class CredentialResolverDataNotFoundError extends CredentialResolverError {
	constructor() {
		super('No data found available for the requested credential and context combination.');
		this.name = 'CredentialResolverDataNotFoundError';
	}
}

/**
 * Thrown when resolver configuration validation fails.
 * Indicates invalid configuration values or unreachable external services.
 */
export class CredentialResolverValidationError extends CredentialResolverError {
	constructor(message: string) {
		super(`Credential resolver options validation failed: ${message}`);
		this.name = 'CredentialResolverValidationError';
	}
}
