"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/helpers/constants.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/OpenAi 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:MODELS_NOT_SUPPORT_FUNCTION_CALLS。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/helpers/constants.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/OpenAi/helpers/constants.py

export const MODELS_NOT_SUPPORT_FUNCTION_CALLS = [
	'gpt-3.5-turbo-16k-0613',
	'dall-e-3',
	'text-embedding-3-large',
	'dall-e-2',
	'whisper-1',
	'tts-1-hd-1106',
	'tts-1-hd',
	'gpt-4-0314',
	'text-embedding-3-small',
	'gpt-4-32k-0314',
	'gpt-3.5-turbo-0301',
	'gpt-4-vision-preview',
	'gpt-3.5-turbo-16k',
	'gpt-3.5-turbo-instruct-0914',
	'tts-1',
	'davinci-002',
	'gpt-3.5-turbo-instruct',
	'babbage-002',
	'tts-1-1106',
	'text-embedding-ada-002',
];
