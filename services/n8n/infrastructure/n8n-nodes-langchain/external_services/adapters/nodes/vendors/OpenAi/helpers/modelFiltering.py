"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/helpers/modelFiltering.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/OpenAi 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:shouldIncludeModel。关键函数/方法:shouldIncludeModel。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。注释目标:Determines whether a model should be included in the model list based on / whether it's a custom API and the model's ID.。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/helpers/modelFiltering.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/OpenAi/helpers/modelFiltering.py

/**
 * Determines whether a model should be included in the model list based on
 * whether it's a custom API and the model's ID.
 *
 * @param modelId - The ID of the model to check
 * @param isCustomAPI - Whether this is a custom API (not official OpenAI)
 * @returns true if the model should be included, false otherwise
 */
export function shouldIncludeModel(modelId: string, isCustomAPI: boolean): boolean {
	// For custom APIs, include all models
	if (isCustomAPI) {
		return true;
	}

	// For official OpenAI API, exclude certain model types
	return !(
		modelId.startsWith('babbage') ||
		modelId.startsWith('davinci') ||
		modelId.startsWith('computer-use') ||
		modelId.startsWith('dall-e') ||
		modelId.startsWith('text-embedding') ||
		modelId.startsWith('tts') ||
		modelId.includes('-tts') ||
		modelId.startsWith('whisper') ||
		modelId.startsWith('omni-moderation') ||
		modelId.startsWith('sora') ||
		modelId.includes('-realtime') ||
		(modelId.startsWith('gpt-') && modelId.includes('instruct'))
	);
}
