"""
MIGRATION-META:
  source_path: packages/cli/src/credentials/dynamic-credential-storage.interface.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:无。导出:CredentialStoreMetadata、IDynamicCredentialStorageProvider。关键函数/方法:storeIfNeeded。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Credential resolution/storage ports -> application/ports/outbound/credentials
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/credentials/dynamic-credential-storage.interface.ts -> services/n8n/application/cli/ports/outbound/credentials/dynamic_credential_storage_interface.py

import type {
	ICredentialContext,
	ICredentialDataDecryptedObject,
	IWorkflowSettings,
} from 'n8n-workflow';

/**
 * Metadata for storing credentials to external systems.
 */
export type CredentialStoreMetadata = {
	/** Credential ID */
	id: string;
	/** Credential name */
	name: string;
	/** Credential type (e.g., 'oAuth2Api') */
	type: string;
	/** Resolver ID to use for storage */
	resolverId?: string;
	/** Whether credential supports dynamic storage */
	isResolvable: boolean;
};

/**
 * Provider for storing credentials to external secret management systems.
 * Handles the write path for dynamic credentials (e.g., OAuth token refresh).
 */
export interface IDynamicCredentialStorageProvider {
	/**
	 * Stores credential data to external system if credential is configured for dynamic storage.
	 *
	 * @param credentialStoreMetadata Credential metadata
	 * @param dynamicData Credential data to store (e.g., tokens)
	 * @param credentialContext Identity and metadata for scoping storage
	 * @param staticData Static credential data from database (e.g., clientId, clientSecret)
	 * @param workflowSettings Workflow settings with fallback resolver ID
	 */
	storeIfNeeded(
		credentialStoreMetadata: CredentialStoreMetadata,
		dynamicData: ICredentialDataDecryptedObject,
		credentialContext: ICredentialContext,
		staticData?: ICredentialDataDecryptedObject,
		workflowSettings?: IWorkflowSettings,
	): Promise<void>;
}
