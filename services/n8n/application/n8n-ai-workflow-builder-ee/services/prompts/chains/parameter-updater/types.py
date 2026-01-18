"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater/types.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater 的工作流类型。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:NodeTypePattern、PromptContext、NodeTypeGuide、NodeTypeExamples。关键函数/方法:无。用于定义工作流相关类型/结构约束，供多模块共享。注释目标:Types for the parameter-updater prompt registry system. / This module defines the interfaces for registering node-type specific。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater/types.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/prompts/chains/parameter-updater/types.py

/**
 * Types for the parameter-updater prompt registry system.
 *
 * This module defines the interfaces for registering node-type specific
 * guides and examples that are automatically matched based on patterns.
 */

import type { INodeTypeDescription } from 'n8n-workflow';

/**
 * Pattern for matching node types. Supports:
 * - Exact match: 'n8n-nodes-base.set'
 * - Suffix wildcard: '*Tool' matches 'gmailTool', 'slackTool'
 * - Prefix wildcard: 'n8n-nodes-base.*' matches any n8n-nodes-base node
 * - Substring match: '.set' matches 'n8n-nodes-base.set'
 */
export type NodeTypePattern = string;

/**
 * Context passed to conditional guides/examples for matching decisions.
 */
export interface PromptContext {
	/** The node type string (e.g., 'n8n-nodes-base.set') */
	nodeType: string;
	/** The full node type definition */
	nodeDefinition: INodeTypeDescription;
	/** The requested changes from the user */
	requestedChanges: string[];
	/** Whether node has resource locator parameters */
	hasResourceLocatorParams?: boolean;
}

/**
 * A registered guide for specific node types.
 */
export interface NodeTypeGuide {
	/** Patterns to match against node type (any match triggers inclusion) */
	patterns: NodeTypePattern[];
	/** Guide content string */
	content: string;
	/**
	 * Optional condition function for more complex matching logic.
	 * If provided, guide is only included if condition returns true.
	 */
	condition?: (context: PromptContext) => boolean;
}

/**
 * Registered examples for specific node types.
 */
export interface NodeTypeExamples {
	/** Patterns to match against node type (any match triggers inclusion) */
	patterns: NodeTypePattern[];
	/** Examples content string */
	content: string;
	/**
	 * Optional condition function for more complex matching logic.
	 */
	condition?: (context: PromptContext) => boolean;
}
