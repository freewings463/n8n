"""
MIGRATION-META:
  source_path: packages/core/src/binary-data/binary-data.config.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/core/src/binary-data 的配置。导入/依赖:外部:zod；内部:@n8n/config、@/instance-settings；本地:无。导出:BINARY_DATA_MODES、BinaryDataConfig。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Core binary-data storage -> infrastructure file_storage adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/binary-data/binary-data.config.ts -> services/n8n/infrastructure/core/external_services/adapters/file_storage/binary_data/binary_data_config.py

import { Config, Env, ExecutionsConfig } from '@n8n/config';
import { createHash } from 'node:crypto';
import path from 'node:path';
import { z } from 'zod';

import { InstanceSettings } from '@/instance-settings';

export const BINARY_DATA_MODES = ['default', 'filesystem', 's3', 'database'] as const;

const binaryDataModesSchema = z.enum(BINARY_DATA_MODES);

const availableModesSchema = z
	.string()
	.transform((value) => value.split(','))
	.pipe(binaryDataModesSchema.array());

const dbMaxFileSizeSchema = z.coerce
	.number()
	.max(1024, 'Binary data max file size in `database` mode cannot exceed 1024 MiB'); // because of Postgres BYTEA hard limit

@Config
export class BinaryDataConfig {
	/** Available modes of binary data storage, as comma separated strings. */
	availableModes: z.infer<typeof availableModesSchema> = ['filesystem', 's3', 'database'];

	/** Storage mode for binary data. Defaults to 'filesystem' in regular mode, 'database' in scaling mode. */
	@Env('N8N_DEFAULT_BINARY_DATA_MODE', binaryDataModesSchema)
	mode!: z.infer<typeof binaryDataModesSchema>;

	/** Path for binary data storage in "filesystem" mode. */
	@Env('N8N_BINARY_DATA_STORAGE_PATH')
	localStoragePath: string;

	/**
	 * Secret for creating publicly-accesible signed URLs for binary data.
	 * When not passed in, this will be derived from the instances's encryption-key
	 **/
	@Env('N8N_BINARY_DATA_SIGNING_SECRET')
	signingSecret: string;

	/** Maximum file size (in MiB) for binary data in `database` mode. **/
	@Env('N8N_BINARY_DATA_DATABASE_MAX_FILE_SIZE', dbMaxFileSizeSchema)
	dbMaxFileSize: number = 512;

	constructor({ encryptionKey, n8nFolder }: InstanceSettings, executionsConfig: ExecutionsConfig) {
		this.localStoragePath = path.join(n8nFolder, 'binaryData');
		this.signingSecret = createHash('sha256')
			.update(`url-signing:${encryptionKey}`)
			.digest('base64');

		this.mode ??= executionsConfig.mode === 'queue' ? 'database' : 'filesystem';
	}
}
