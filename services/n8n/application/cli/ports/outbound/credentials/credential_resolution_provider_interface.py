"""
MIGRATION-META:
  source_path: packages/cli/src/credentials/credential-resolution-provider.interface.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:CredentialResolveMetadata、ICredentialResolutionProvider。关键函数/方法:resolveIfNeeded。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Credential resolution/storage ports -> application/ports/outbound/credentials
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/credentials/credential-resolution-provider.interface.ts -> services/n8n/application/cli/ports/outbound/credentials/credential_resolution_provider_interface.py

import type {
	ICredentialDataDecryptedObject,
	IExecutionContext,
	IWorkflowSettings,
} from 'n8n-workflow';

export type CredentialResolveMetadata = {
	id: string;
	name: string;
	/** Credential type (e.g., 'oAuth2Api') */
	type: string;
	resolverId?: string;
	resolvableAllowFallback?: boolean;
	isResolvable: boolean;
};

/**
 * Interface for credential resolution providers.
 * Implementations can provide dynamic credential resolution logic.
 * This allows EE modules to hook into credential resolution without tight coupling.
 */
export interface ICredentialResolutionProvider {
	/**
	 * Resolves credentials dynamically if configured, otherwise returns static data.
	 *
	 * @param credentialsResolveMetadata The credential resolve metadata
	 * @param staticData The decrypted static credential data
	 * @param additionalData Additional workflow execution data for context and settings
	 * @param canUseExternalSecrets Whether the credential can use external secrets for expression resolution
	 * @returns Resolved credential data (either dynamic or static)
	 */
	resolveIfNeeded(
		credentialsResolveMetadata: CredentialResolveMetadata,
		staticData: ICredentialDataDecryptedObject,
		executionContext?: IExecutionContext,
		workflowSettings?: IWorkflowSettings,
		canUseExternalSecrets?: boolean,
	): Promise<ICredentialDataDecryptedObject>;
}
