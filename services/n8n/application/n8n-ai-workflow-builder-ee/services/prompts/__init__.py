"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/prompts/index.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/prompts 的工作流入口。导入/依赖:外部:无；内部:无；本地:无。导出:buildBuilderPrompt、buildConfiguratorPrompt、INSTANCE_URL_PROMPT、buildSupervisorPrompt、buildResponderPrompt、compactPromptTemplate 等1项。关键函数/方法:无。用于汇总导出并完成工作流模块初始化、注册或装配。注释目标:Centralized prompts for AI Workflow Builder / This directory contains all prompts used by the AI workflow builder agents and chains.。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/prompts/index.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/prompts/__init__.py

/**
 * Centralized prompts for AI Workflow Builder
 *
 * This directory contains all prompts used by the AI workflow builder agents and chains.
 * Organization:
 * - builder/ - PromptBuilder utility for composing prompts
 * - agents/ - Multi-agent system prompts (builder, configurator, discovery, etc.)
 * - chains/ - Chain-level prompts (categorization, compact, workflow-name, parameter-updater)
 * - legacy-agent.prompt.ts - Legacy single-agent mode prompt
 */

// Prompt builder utility
export {
	PromptBuilder,
	prompt,
	type ContentOrFactory,
	type MessageBlock,
	type PromptBuilderOptions,
	type SectionFormat,
	type SectionOptions,
} from './builder';

// Agent prompts (multi-agent system)
export { buildBuilderPrompt } from './agents/builder.prompt';
export {
	buildDiscoveryPrompt,
	formatTechniqueList,
	formatExampleCategorizations,
	type DiscoveryPromptOptions,
} from './agents/discovery.prompt';
export { buildConfiguratorPrompt, INSTANCE_URL_PROMPT } from './agents/configurator.prompt';
export { buildSupervisorPrompt } from './agents/supervisor.prompt';
export { buildResponderPrompt } from './agents/responder.prompt';

// Legacy agent prompt (single-agent mode)
export {
	createMainAgentPrompt,
	mainAgentPrompt,
	type MainAgentPromptOptions,
} from './legacy-agent.prompt';

// Chain prompts
export {
	promptCategorizationTemplate,
	examplePrompts,
	formatExamplePrompts,
	formatTechniqueList as formatCategorizationTechniqueList,
} from './chains/categorization.prompt';
export { compactPromptTemplate } from './chains/compact.prompt';
export { workflowNamingPromptTemplate } from './chains/workflow-name.prompt';

// Parameter updater prompts
export {
	// Registry system
	getMatchingGuides,
	getMatchingExamples,
	matchesPattern,
	// Utilities
	hasResourceLocatorParameters,
	instanceUrlPrompt,
	// Base prompts
	CORE_INSTRUCTIONS,
	EXPRESSION_RULES,
	COMMON_PATTERNS,
	OUTPUT_FORMAT,
	// Node-type guides
	SET_NODE_GUIDE,
	IF_NODE_GUIDE,
	SWITCH_NODE_GUIDE,
	HTTP_REQUEST_GUIDE,
	TOOL_NODES_GUIDE,
	RESOURCE_LOCATOR_GUIDE,
	SYSTEM_MESSAGE_GUIDE,
	TEXT_FIELDS_GUIDE,
} from './chains/parameter-updater';

export type {
	NodeTypeGuide,
	NodeTypeExamples,
	NodeTypePattern,
	PromptContext,
} from './chains/parameter-updater';
