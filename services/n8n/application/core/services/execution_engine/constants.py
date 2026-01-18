"""
MIGRATION-META:
  source_path: packages/core/src/constants.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src 的模块。导入/依赖:外部:无；内部:无；本地:无。导出:CUSTOM_EXTENSION_ENV、PLACEHOLDER_EMPTY_EXECUTION_ID、PLACEHOLDER_EMPTY_WORKFLOW_ID、HTTP_REQUEST_NODE_TYPE、HTTP_REQUEST_AS_TOOL_NODE_TYPE、HTTP_REQUEST_TOOL_NODE_TYPE、RESTRICT_FILE_ACCESS_TO、BLOCK_FILE_ACCESS_TO_N8N_FILES 等6项。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Core src/* defaulted to execution engine application services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/constants.ts -> services/n8n/application/core/services/execution_engine/constants.py

export const CUSTOM_EXTENSION_ENV = 'N8N_CUSTOM_EXTENSIONS';
export const PLACEHOLDER_EMPTY_EXECUTION_ID = '__UNKNOWN__';
export const PLACEHOLDER_EMPTY_WORKFLOW_ID = '__EMPTY__';
export const HTTP_REQUEST_NODE_TYPE = 'n8n-nodes-base.httpRequest';
export const HTTP_REQUEST_AS_TOOL_NODE_TYPE = 'n8n-nodes-base.httpRequestTool';
export const HTTP_REQUEST_TOOL_NODE_TYPE = '@n8n/n8n-nodes-langchain.toolHttpRequest';

export const RESTRICT_FILE_ACCESS_TO = 'N8N_RESTRICT_FILE_ACCESS_TO';
export const BLOCK_FILE_ACCESS_TO_N8N_FILES = 'N8N_BLOCK_FILE_ACCESS_TO_N8N_FILES';
export const CONFIG_FILES = 'N8N_CONFIG_FILES';
export const BINARY_DATA_STORAGE_PATH = 'N8N_BINARY_DATA_STORAGE_PATH';
export const UM_EMAIL_TEMPLATES_INVITE = 'N8N_UM_EMAIL_TEMPLATES_INVITE';
export const UM_EMAIL_TEMPLATES_PWRESET = 'N8N_UM_EMAIL_TEMPLATES_PWRESET';

export const CREDENTIAL_ERRORS = {
	NO_DATA: 'No data is set on this credentials.',
	DECRYPTION_FAILED:
		'Credentials could not be decrypted. The likely reason is that a different "encryptionKey" was used to encrypt the data.',
	INVALID_JSON: 'Decrypted credentials data is not valid JSON.',
	INVALID_DATA: 'Credentials data is not in a valid format.',
};

export const WAITING_TOKEN_QUERY_PARAM = 'signature';
