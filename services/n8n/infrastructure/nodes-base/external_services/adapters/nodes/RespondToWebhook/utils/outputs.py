"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/RespondToWebhook/utils/outputs.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/RespondToWebhook/utils 的工具。导入/依赖:外部:无；内部:无；本地:无。导出:configuredOutputs。关键函数/方法:configuredOutputs。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/RespondToWebhook/utils/outputs.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/RespondToWebhook/utils/outputs.py

export const configuredOutputs = (
	version: number,
	parameters: { enableResponseOutput?: boolean },
) => {
	const multipleOutputs = version === 1.3 || (version >= 1.4 && parameters.enableResponseOutput);
	if (multipleOutputs) {
		return [
			{
				type: 'main',
				displayName: 'Input Data',
			},
			{
				type: 'main',
				displayName: 'Response',
			},
		];
	}

	return ['main'];
};
