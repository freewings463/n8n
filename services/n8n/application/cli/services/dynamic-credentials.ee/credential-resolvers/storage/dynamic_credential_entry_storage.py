"""
MIGRATION-META:
  source_path: packages/cli/src/modules/dynamic-credentials.ee/credential-resolvers/storage/dynamic-credential-entry-storage.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/dynamic-credentials.ee/credential-resolvers 的模块。导入/依赖:外部:无；内部:@n8n/di、@n8n/decorators；本地:./storage-interface、../entities/dynamic-credential-entry、../repositories/dynamic-credential-entry.repository。导出:DynamicCredentialEntryStorage。关键函数/方法:getCredentialData、setCredentialData、deleteCredentialData、deleteAllCredentialData。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/dynamic-credentials.ee/credential-resolvers/storage/dynamic-credential-entry-storage.ts -> services/n8n/application/cli/services/dynamic-credentials.ee/credential-resolvers/storage/dynamic_credential_entry_storage.py

import { Service } from '@n8n/di';

import { ICredentialEntriesStorage } from './storage-interface';
import { DynamicCredentialEntry } from '../../database/entities/dynamic-credential-entry';
import { DynamicCredentialEntryRepository } from '../../database/repositories/dynamic-credential-entry.repository';
import { CredentialResolverHandle } from '@n8n/decorators';

@Service()
export class DynamicCredentialEntryStorage implements ICredentialEntriesStorage {
	constructor(
		private readonly dynamicCredentialEntryRepository: DynamicCredentialEntryRepository,
	) {}

	async getCredentialData(
		credentialId: string,
		subjectId: string,
		resolverId: string,
		_: Record<string, unknown>,
	): Promise<string | null> {
		const entry = await this.dynamicCredentialEntryRepository.findOne({
			where: {
				credentialId,
				subjectId,
				resolverId,
			},
		});

		return entry?.data ?? null;
	}

	async setCredentialData(
		credentialId: string,
		subjectId: string,
		resolverId: string,
		data: string,
		_: Record<string, unknown>,
	): Promise<void> {
		let entry = await this.dynamicCredentialEntryRepository.findOne({
			where: { credentialId, subjectId, resolverId },
		});

		if (!entry) {
			entry = new DynamicCredentialEntry();
			entry.credentialId = credentialId;
			entry.subjectId = subjectId;
			entry.resolverId = resolverId;
		}

		entry.data = data;
		await this.dynamicCredentialEntryRepository.save(entry);
	}

	async deleteCredentialData(
		credentialId: string,
		subjectId: string,
		resolverId: string,
		_: Record<string, unknown>,
	): Promise<void> {
		await this.dynamicCredentialEntryRepository.delete({
			credentialId,
			subjectId,
			resolverId,
		});
	}

	async deleteAllCredentialData(handle: CredentialResolverHandle): Promise<void> {
		await this.dynamicCredentialEntryRepository.delete({ resolverId: handle.resolverId });
	}
}
