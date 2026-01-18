"""
MIGRATION-META:
  source_path: packages/core/src/binary-data/object-store.manager.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/binary-data 的Store。导入/依赖:外部:node:fs/promises、uuid；内部:@n8n/di；本地:./object-store/object-store.service.ee、./types、./utils。导出:ObjectStoreManager。关键函数/方法:init、store、getPath、getAsBuffer、getAsStream、getMetadata、copyByFileId、copyByFilePath、rename、toFileId。用于管理该模块前端状态（state/actions/getters）供UI消费。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/binary-data/object-store.manager.ts -> services/n8n/application/core/services/binary-data/object_store_manager.py

import { Service } from '@n8n/di';
import fs from 'node:fs/promises';
import type { Readable } from 'node:stream';
import { v4 as uuid } from 'uuid';

import { ObjectStoreService } from './object-store/object-store.service.ee';
import type { BinaryData } from './types';
import { binaryToBuffer } from './utils';

@Service()
export class ObjectStoreManager implements BinaryData.Manager {
	constructor(private readonly objectStoreService: ObjectStoreService) {}

	async init() {
		await this.objectStoreService.checkConnection();
	}

	async store(
		location: BinaryData.FileLocation,
		bufferOrStream: Buffer | Readable,
		metadata: BinaryData.PreWriteMetadata,
	) {
		const fileId = this.toFileId(location);
		const buffer = await binaryToBuffer(bufferOrStream);

		await this.objectStoreService.put(fileId, buffer, metadata);

		return { fileId, fileSize: buffer.length };
	}

	getPath(fileId: string) {
		return fileId; // already full path, no transform needed
	}

	async getAsBuffer(fileId: string) {
		return await this.objectStoreService.get(fileId, { mode: 'buffer' });
	}

	async getAsStream(fileId: string) {
		return await this.objectStoreService.get(fileId, { mode: 'stream' });
	}

	async getMetadata(fileId: string): Promise<BinaryData.Metadata> {
		const {
			'content-length': contentLength,
			'content-type': contentType,
			'x-amz-meta-filename': fileName,
		} = await this.objectStoreService.getMetadata(fileId);

		const metadata: BinaryData.Metadata = { fileSize: Number(contentLength) };

		if (contentType) metadata.mimeType = contentType;
		if (fileName) metadata.fileName = fileName;

		return metadata;
	}

	async copyByFileId(targetLocation: BinaryData.FileLocation, sourceFileId: string) {
		const targetFileId = this.toFileId(targetLocation);

		const sourceFile = await this.objectStoreService.get(sourceFileId, { mode: 'buffer' });

		await this.objectStoreService.put(targetFileId, sourceFile);

		return targetFileId;
	}

	/**
	 * Copy to object store the temp file written by nodes like Webhook, FTP, and SSH.
	 */
	async copyByFilePath(
		targetLocation: BinaryData.FileLocation,
		sourcePath: string,
		metadata: BinaryData.PreWriteMetadata,
	) {
		const targetFileId = this.toFileId(targetLocation);
		const sourceFile = await fs.readFile(sourcePath);

		await this.objectStoreService.put(targetFileId, sourceFile, metadata);

		return { fileId: targetFileId, fileSize: sourceFile.length };
	}

	async rename(oldFileId: string, newFileId: string) {
		const oldFile = await this.objectStoreService.get(oldFileId, { mode: 'buffer' });
		const oldFileMetadata = await this.objectStoreService.getMetadata(oldFileId);

		await this.objectStoreService.put(newFileId, oldFile, oldFileMetadata);
		await this.objectStoreService.deleteOne(oldFileId);
	}

	// ----------------------------------
	//         private methods
	// ----------------------------------

	private toFileId(location: BinaryData.FileLocation) {
		switch (location.type) {
			case 'execution': {
				const executionId = location.executionId || 'temp'; // missing only in edge case, see PR #7244
				return `workflows/${location.workflowId}/executions/${executionId}/binary_data/${uuid()}`;
			}
			case 'custom':
				return `${location.pathSegments.join('/')}/binary_data/${uuid()}`;
		}
	}
}
