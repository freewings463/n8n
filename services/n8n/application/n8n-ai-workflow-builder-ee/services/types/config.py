"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/types/config.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/types 的工作流类型。导入/依赖:外部:@langchain/core/tools；内部:n8n-workflow、@/workflow-state；本地:无。导出:LLMConfig、ParameterUpdaterOptions、NodePromptConfig、PromptGenerationOptions、PromptBuilderContext、ToolExecutorOptions。关键函数/方法:无。用于定义工作流相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/types/config.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/types/config.py

import type { DynamicStructuredTool } from '@langchain/core/tools';
import type { INodeTypeDescription } from 'n8n-workflow';

import type { WorkflowState } from '@/workflow-state';

/**
 * LLM configuration for the workflow builder
 */
export interface LLMConfig {
	openAIApiKey?: string;
	model: string;
	temperature?: number;
}

/**
 * Options for parameter updater chain
 */
export interface ParameterUpdaterOptions {
	nodeType: string;
	nodeDefinition: INodeTypeDescription;
	requestedChanges: string[];
}

/**
 * Configuration for mapping node types to required prompt sections
 */
export interface NodePromptConfig {
	/** Node type patterns that require specific guides */
	nodeTypePatterns: {
		set: string[];
		if: string[];
		switch: string[];
		httpRequest: string[];
		tool: string[];
		gmail: string[];
	};

	/** Keywords that trigger inclusion of specific guides */
	parameterKeywords: {
		resourceLocator: string[];
		textExpressions: string[];
	};

	/** Maximum number of examples to include */
	maxExamples: number;

	/** Token budget for dynamic sections */
	targetTokenBudget: number;
}

/**
 * Advanced configuration for fine-tuning prompt generation
 */
export interface PromptGenerationOptions {
	/** Include examples in the prompt */
	includeExamples?: boolean;

	/** Override the maximum number of examples */
	maxExamples?: number;

	/** Force inclusion of specific guides */
	forceInclude?: {
		setNode?: boolean;
		ifNode?: boolean;
		httpRequest?: boolean;
		toolNodes?: boolean;
		resourceLocator?: boolean;
		textFields?: boolean;
	};

	/** Custom token budget */
	tokenBudget?: number;

	/** Enable verbose logging */
	verbose?: boolean;
}

/**
 * Context for building prompts
 */
export interface PromptBuilderContext {
	nodeType: string;
	nodeDefinition: INodeTypeDescription;
	requestedChanges: string[];
	hasResourceLocatorParams?: boolean;
	options?: PromptGenerationOptions;
	config?: NodePromptConfig;
}

/**
 * Options for tool executor
 */
export interface ToolExecutorOptions {
	state: typeof WorkflowState.State;
	toolMap: Map<string, DynamicStructuredTool>;
}
