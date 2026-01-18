"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/tools/utils/node-creation.utils.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/tools/utils 的工作流工具。导入/依赖:外部:无；内部:无；本地:无。导出:generateUniqueName、getLatestVersion、generateNodeId、generateWebhookId、requiresWebhook、createNodeInstance、mergeWithDefaults。关键函数/方法:generateUniqueName、getLatestVersion、generateNodeId、generateWebhookId、requiresWebhook、createNodeInstance、assert、mergeWithDefaults。用于提供工作流通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/tools/utils/node-creation.utils.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/tools/utils/node_creation_utils.py

import {
	assert,
	type INode,
	type INodeTypeDescription,
	type NodeParameterValueType,
} from 'n8n-workflow';

/**
 * Generate a unique node name by appending numbers if necessary
 * @param baseName - The base name to start with
 * @param existingNodes - Array of existing nodes to check against
 * @returns A unique node name
 */
export function generateUniqueName(baseName: string, existingNodes: INode[]): string {
	let uniqueName = baseName;
	let counter = 1;

	while (existingNodes.some((n) => n.name === uniqueName)) {
		uniqueName = `${baseName}${counter}`;
		counter++;
	}

	return uniqueName;
}

/**
 * Get the latest version number for a node type
 * @param nodeType - The node type description
 * @returns The latest version number
 */
export function getLatestVersion(nodeType: INodeTypeDescription): number {
	return (
		nodeType.defaultVersion ??
		(typeof nodeType.version === 'number'
			? nodeType.version
			: nodeType.version[nodeType.version.length - 1])
	);
}

/**
 * Generate a unique node ID
 * @returns A unique node identifier
 */
export function generateNodeId(): string {
	return crypto.randomUUID();
}

/**
 * Generate a webhook ID for nodes that require it
 * @returns A unique webhook identifier
 */
export function generateWebhookId(): string {
	return crypto.randomUUID();
}

/**
 * Check if a node type requires a webhook
 * @param nodeType - The node type description
 * @returns True if the node requires a webhook
 */
export function requiresWebhook(nodeType: INodeTypeDescription): boolean {
	return !!(nodeType.webhooks && nodeType.webhooks.length > 0);
}

/**
 * Create a new node instance with all required properties
 * @param nodeType - The node type description
 * @param typeVersion - The node type version - nodeType can have multiple versions
 * @param name - The name for the node
 * @param position - The position of the node
 * @param parameters - Optional parameters for the node
 * @param id - Optional specific ID to use for the node (for testing purposes)
 * @returns A complete node instance
 */
export function createNodeInstance(
	nodeType: INodeTypeDescription,
	typeVersion: number,
	name: string,
	position: [number, number],
	parameters: Record<string, NodeParameterValueType> = {},
	id?: string,
): INode {
	assert(
		Array.isArray(nodeType.version)
			? nodeType.version.includes(typeVersion)
			: typeVersion === nodeType.version,
	);
	const node: INode = {
		id: id ?? generateNodeId(),
		name,
		type: nodeType.name,
		typeVersion,
		position,
		parameters,
	};

	// Add webhook ID if required
	if (requiresWebhook(nodeType)) {
		node.webhookId = generateWebhookId();
	}

	return node;
}

/**
 * Merge provided parameters with node defaults
 * @param parameters - User-provided parameters
 * @param nodeType - The node type description
 * @returns Merged parameters
 */
export function mergeWithDefaults(
	parameters: Record<string, NodeParameterValueType>,
	nodeType: INodeTypeDescription,
): Record<string, NodeParameterValueType> {
	const defaults = nodeType.defaults || {};
	return { ...defaults, ...parameters };
}
