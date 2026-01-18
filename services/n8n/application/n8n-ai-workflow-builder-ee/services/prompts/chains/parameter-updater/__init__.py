"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater/index.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater 的工作流入口。导入/依赖:外部:无；内部:无；本地:无。导出:getMatchingGuides、getMatchingExamples、matchesPattern、hasResourceLocatorParameters、instanceUrlPrompt。关键函数/方法:无。用于汇总导出并完成工作流模块初始化、注册或装配。注释目标:Registry system。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater/index.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/prompts/chains/parameter-updater/__init__.py

// Registry system
export { getMatchingGuides, getMatchingExamples, matchesPattern } from './registry';
export type {
	NodeTypeGuide,
	NodeTypeExamples,
	NodeTypePattern,
	PromptContext,
} from './types';

// Utilities
export { hasResourceLocatorParameters } from './utils';
export { instanceUrlPrompt } from './instance-url';

// Base prompts
export {
	CORE_INSTRUCTIONS,
	EXPRESSION_RULES,
	COMMON_PATTERNS,
	OUTPUT_FORMAT,
} from './parameter-updater.prompt';

// Node type guides
export {
	SET_NODE_GUIDE,
	IF_NODE_GUIDE,
	SWITCH_NODE_GUIDE,
	HTTP_REQUEST_GUIDE,
	TOOL_NODES_GUIDE,
	GMAIL_GUIDE,
} from './guides';

// Parameter type guides
export {
	RESOURCE_LOCATOR_GUIDE,
	SYSTEM_MESSAGE_GUIDE,
	TEXT_FIELDS_GUIDE,
} from './guides';

// Examples
export {
	SET_NODE_EXAMPLES,
	IF_NODE_EXAMPLES,
	SWITCH_NODE_EXAMPLES,
	SIMPLE_UPDATE_EXAMPLES,
	TOOL_NODE_EXAMPLES,
	RESOURCE_LOCATOR_EXAMPLES,
} from './examples';
