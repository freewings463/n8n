"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater/utils.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater 的工作流模块。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:hasResourceLocatorParameters。关键函数/方法:hasResourceLocatorParameters、checkProperties。用于承载工作流实现细节，并通过导出对外提供能力。注释目标:Utility functions for parameter updater prompts.。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater/utils.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/prompts/chains/parameter-updater/utils.py

/**
 * Utility functions for parameter updater prompts.
 */

import type { INodeTypeDescription, INodeProperties } from 'n8n-workflow';

/**
 * Analyzes node definition to determine if it has resource locator parameters.
 */
export function hasResourceLocatorParameters(nodeDefinition: INodeTypeDescription): boolean {
	if (!nodeDefinition.properties) return false;

	const checkProperties = (properties: INodeProperties[]): boolean => {
		for (const prop of properties) {
			if (prop.type === 'resourceLocator' || prop.type === 'fixedCollection') return true;
		}
		return false;
	};

	return checkProperties(nodeDefinition.properties);
}
