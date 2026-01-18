"""
MIGRATION-META:
  source_path: packages/core/src/binary-data/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/core/src/binary-data 的类型。导入/依赖:外部:无；内部:无；本地:./binary-data.config。导出:ConfigMode、ServiceMode、StoredMode、Metadata、WriteResult、PreWriteMetadata、FileLocation、Manager 等1项。关键函数/方法:init、store、getPath、getAsBuffer、getAsStream、getMetadata、copyByFileId、copyByFilePath、rename。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Core binary-data storage -> infrastructure file_storage adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/binary-data/types.ts -> services/n8n/infrastructure/core/external_services/adapters/file_storage/binary_data/types.py

import type { Readable } from 'stream';

import type { BINARY_DATA_MODES } from './binary-data.config';

export namespace BinaryData {
	type LegacyMode = 'filesystem';

	type UpgradedMode = 'filesystem-v2';

	/**
	 * Binary data mode selectable by user via env var config.
	 */
	export type ConfigMode = (typeof BINARY_DATA_MODES)[number];

	/**
	 * Binary data mode used internally by binary data service. User-selected
	 * legacy modes are replaced with upgraded modes.
	 */
	export type ServiceMode = Exclude<ConfigMode, LegacyMode> | UpgradedMode;

	/**
	 * Binary data mode in binary data ID in stored execution data. Both legacy
	 * and upgraded modes may be present, except default in-memory mode.
	 */
	export type StoredMode = Exclude<ConfigMode | UpgradedMode, 'default'>;

	export type Metadata = {
		fileName?: string;
		mimeType?: string;
		fileSize: number;
	};

	export type WriteResult = { fileId: string; fileSize: number };

	export type PreWriteMetadata = Omit<Metadata, 'fileSize'>;

	export type FileLocation =
		| { type: 'execution'; workflowId: string; executionId: string }
		| { type: 'custom'; pathSegments: string[]; sourceType?: string; sourceId?: string };

	export interface Manager {
		init(): Promise<void>;

		store(
			location: FileLocation,
			bufferOrStream: Buffer | Readable,
			metadata: PreWriteMetadata,
		): Promise<WriteResult>;

		getPath(fileId: string): string;
		getAsBuffer(fileId: string): Promise<Buffer>;
		getAsStream(fileId: string, chunkSize?: number): Promise<Readable>;
		getMetadata(fileId: string): Promise<Metadata>;

		/**
		 * Present for `FileSystem`, absent for `ObjectStore` (delegated to S3 lifecycle config)
		 */
		deleteMany?(locations: FileLocation[]): Promise<void>;
		deleteManyByFileId?(ids: string[]): Promise<void>;

		copyByFileId(targetLocation: FileLocation, sourceFileId: string): Promise<string>;
		copyByFilePath(
			targetLocation: FileLocation,
			sourcePath: string,
			metadata: PreWriteMetadata,
		): Promise<WriteResult>;

		rename(oldFileId: string, newFileId: string): Promise<void>;
	}

	export type SigningPayload = {
		id: string;
	};
}
