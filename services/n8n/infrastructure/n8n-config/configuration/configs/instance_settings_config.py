"""
MIGRATION-META:
  source_path: packages/@n8n/config/src/configs/instance-settings-config.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/config/src/configs 的配置。导入/依赖:外部:无；内部:无；本地:../decorators、../utils/utils。导出:InstanceSettingsConfig。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/config treated as infrastructure configuration/runtime environment
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/config/src/configs/instance-settings-config.ts -> services/n8n/infrastructure/n8n-config/configuration/configs/instance_settings_config.py

import path from 'node:path';

import { Config, Env } from '../decorators';
import { getN8nFolder } from '../utils/utils';

@Config
export class InstanceSettingsConfig {
	/**
	 * Whether to enforce that n8n settings file doesn't have overly wide permissions.
	 * If set to true, n8n will check the permissions of the settings file and
	 * attempt change them to 0600 (only owner has rw access) if they are too wide.
	 */
	@Env('N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS')
	enforceSettingsFilePermissions: boolean = true;

	/**
	 * Encryption key to use for encrypting and decrypting credentials.
	 * If none is provided, a random key will be generated and saved to the settings file on the first launch.
	 * Can be provided directly via N8N_ENCRYPTION_KEY or via a file path using N8N_ENCRYPTION_KEY_FILE.
	 */
	@Env('N8N_ENCRYPTION_KEY')
	encryptionKey: string = '';

	/**
	 * The home folder path of the user.
	 * If none can be found it falls back to the current working directory
	 */
	readonly userHome: string;

	readonly n8nFolder: string;

	constructor() {
		this.n8nFolder = getN8nFolder();
		this.userHome = path.dirname(this.n8nFolder);
	}
}
