"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/types/node-guidance.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/types 的工作流类型。导入/依赖:外部:无；内部:无；本地:无。导出:NodeGuidance。关键函数/方法:无。用于定义工作流相关类型/结构约束，供多模块共享。注释目标:Structured guidance for node usage across different agents. / Each property maps to a specific agent's needs.。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/types/node-guidance.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/types/node_guidance.py

/**
 * Structured guidance for node usage across different agents.
 * Each property maps to a specific agent's needs.
 */
export interface NodeGuidance {
	/** Node identifier (e.g., "@n8n/n8n-nodes-langchain.outputParserStructured") */
	nodeType: string;

	/**
	 * When to use this node - used by Discovery Agent
	 * Describes scenarios/conditions that warrant searching for this node
	 */
	usage: string;

	/**
	 * How to connect this node - used by Builder Agent
	 * Describes connection patterns, source/target relationships
	 */
	connections: string;

	/**
	 * How to configure parameters - used by Builder Agent
	 * Describes parameter settings that affect the node or related nodes
	 */
	configuration: string;

	/**
	 * General recommendations - used by Legacy Agent
	 * High-level guidance about when to prefer this node over alternatives
	 */
	recommendation?: string;
}
