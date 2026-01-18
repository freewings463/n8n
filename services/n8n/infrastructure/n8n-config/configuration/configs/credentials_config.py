"""
MIGRATION-META:
  source_path: packages/@n8n/config/src/configs/credentials.config.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/config/src/configs 的配置。导入/依赖:外部:无；内部:无；本地:../decorators。导出:CredentialsConfig。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/config treated as infrastructure configuration/runtime environment
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/config/src/configs/credentials.config.ts -> services/n8n/infrastructure/n8n-config/configuration/configs/credentials_config.py

import { Config, Env, Nested } from '../decorators';

@Config
class CredentialsOverwrite {
	/**
	 * Prefilled data ("overwrite") in credential types. End users cannot view or change this data.
	 * Format: { CREDENTIAL_NAME: { PARAMETER: VALUE }}
	 */
	@Env('CREDENTIALS_OVERWRITE_DATA')
	data: string = '{}';

	/** Internal API endpoint to fetch overwritten credential types from. */
	@Env('CREDENTIALS_OVERWRITE_ENDPOINT')
	endpoint: string = '';

	/** Authentication token for the credentials overwrite endpoint. */
	@Env('CREDENTIALS_OVERWRITE_ENDPOINT_AUTH_TOKEN')
	endpointAuthToken: string = '';

	/** Enable persistence for credentials overwrites. */
	@Env('CREDENTIALS_OVERWRITE_PERSISTENCE')
	persistence: boolean = false;
}

@Config
export class CredentialsConfig {
	/** Default name for credentials */
	@Env('CREDENTIALS_DEFAULT_NAME')
	defaultName: string = 'My credentials';

	@Nested
	overwrite: CredentialsOverwrite;
}
