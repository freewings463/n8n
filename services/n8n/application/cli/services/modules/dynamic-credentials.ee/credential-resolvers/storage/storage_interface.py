"""
MIGRATION-META:
  source_path: packages/cli/src/modules/dynamic-credentials.ee/credential-resolvers/storage/storage-interface.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/dynamic-credentials.ee/credential-resolvers 的模块。导入/依赖:外部:无；内部:无；本地:无。导出:ICredentialEntriesStorage。关键函数/方法:getCredentialData、setCredentialData。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/dynamic-credentials.ee/credential-resolvers/storage/storage-interface.ts -> services/n8n/application/cli/services/modules/dynamic-credentials.ee/credential-resolvers/storage/storage_interface.py

export interface ICredentialEntriesStorage {
	/**
	 * Retrieves credential data for a specific entity from storage.
	 *
	 * @returns The credential data object, or null if not found
	 * @throws {Error} When storage operation fails
	 */
	getCredentialData(
		credentialId: string,
		subjectId: string,
		resolverId: string,
		storageOptions: Record<string, unknown>,
	): Promise<string | null>;

	/**
	 * Stores credential data for a specific entity in storage.
	 * @throws {Error} When storage operation fails
	 */
	setCredentialData(
		credentialId: string,
		subjectId: string,
		resolverId: string,
		data: string,
		storageOptions: Record<string, unknown>,
	): Promise<void>;

	/**
	 * Deletes credential data for a specific entity from storage.
	 * Optional - not all storage implementations support deletion.
	 * @throws {Error} When deletion operation fails
	 */
	deleteCredentialData?(
		credentialId: string,
		subjectId: string,
		resolverId: string,
		storageOptions: Record<string, unknown>,
	): Promise<void>;
}
