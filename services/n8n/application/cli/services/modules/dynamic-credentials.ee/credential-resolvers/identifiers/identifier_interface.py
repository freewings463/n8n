"""
MIGRATION-META:
  source_path: packages/cli/src/modules/dynamic-credentials.ee/credential-resolvers/identifiers/identifier-interface.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/dynamic-credentials.ee/credential-resolvers 的模块。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:IdentifierValidationError、ITokenIdentifier。关键函数/方法:resolve、validateOptions。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/dynamic-credentials.ee/credential-resolvers/identifiers/identifier-interface.ts -> services/n8n/application/cli/services/modules/dynamic-credentials.ee/credential-resolvers/identifiers/identifier_interface.py

import type { ICredentialContext } from 'n8n-workflow';

/**
 * Error thrown when token identifier validation or resolution fails
 */
export class IdentifierValidationError extends Error {}

/**
 * Interface for resolving unique identifiers from credential contexts
 */
export interface ITokenIdentifier {
	/**
	 * Resolves a unique identifier for the entity in the given context
	 *
	 * @param context - Credential context with execution details
	 * @param identifierOptions - Implementation-specific options
	 * @returns Unique identifier string
	 * @throws {IdentifierValidationError} When validation or resolution fails
	 */
	resolve(context: ICredentialContext, identifierOptions: Record<string, unknown>): Promise<string>;

	/**
	 * Validates identifier options before use
	 *
	 * @param identifierOptions - Implementation-specific options
	 * @throws {IdentifierValidationError} When options are invalid
	 */
	validateOptions(identifierOptions: Record<string, unknown>): Promise<void>;
}
