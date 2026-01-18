"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/tools/utils/node-configuration.utils.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/tools/utils 的工作流工具。导入/依赖:外部:无；内部:n8n-workflow、@/constants 等1项；本地:无。导出:collectSingleNodeConfiguration、addNodeConfigurationToMap、collectNodeConfigurationsFromWorkflows、getNodeConfigurationsFromTemplates 等1项。关键函数/方法:collectSingleNodeConfiguration、addNodeConfigurationToMap、collectNodeConfigurationsFromWorkflows、getNodeConfigurationsFromTemplates 等1项。用于提供工作流…
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/tools/utils/node-configuration.utils.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/tools/utils/node_configuration_utils.py

import type { INodeParameters } from 'n8n-workflow';

import { MAX_NODE_EXAMPLE_CHARS } from '@/constants';
import type { NodeConfigurationsMap, NodeConfigurationEntry, WorkflowMetadata } from '@/types';

/**
 * Node structure for configuration collection
 */
interface NodeForConfiguration {
	type: string;
	typeVersion: number;
	parameters: INodeParameters;
}

/**
 * Collect configuration from a single node if it meets size requirements
 * Returns null if the node has no parameters or exceeds size limits
 */
export function collectSingleNodeConfiguration(
	node: NodeForConfiguration,
): NodeConfigurationEntry | null {
	const hasParams = Object.keys(node.parameters).length > 0;
	if (!hasParams) return null;

	const parametersStr = JSON.stringify(node.parameters);
	if (parametersStr.length > MAX_NODE_EXAMPLE_CHARS) return null;

	return {
		version: node.typeVersion,
		parameters: node.parameters,
	};
}

/**
 * Add a node configuration to a configurations map
 * Mutates the map in place for efficiency when processing multiple nodes
 */
export function addNodeConfigurationToMap(
	nodeType: string,
	config: NodeConfigurationEntry,
	configurationsMap: NodeConfigurationsMap,
): void {
	if (!configurationsMap[nodeType]) {
		configurationsMap[nodeType] = [];
	}
	configurationsMap[nodeType].push(config);
}

/**
 * Collect node configurations from multiple workflows
 * Does not generate mermaid diagrams - just extracts node configurations
 */
export function collectNodeConfigurationsFromWorkflows(
	workflows: WorkflowMetadata[],
): NodeConfigurationsMap {
	const configurations: NodeConfigurationsMap = {};

	for (const workflow of workflows) {
		for (const node of workflow.workflow.nodes) {
			// Skip sticky notes
			if (node.type === 'n8n-nodes-base.stickyNote') continue;

			const config = collectSingleNodeConfiguration(node);
			if (config) {
				addNodeConfigurationToMap(node.type, config, configurations);
			}
		}
	}

	return configurations;
}

/**
 * Get node configurations from cached templates on demand.
 * Filters templates containing the node type and extracts matching configurations.
 *
 * @param templates - The cached workflow templates to extract from
 * @param nodeType - The node type to filter by (e.g., 'n8n-nodes-base.telegram')
 * @param nodeVersion - Optional version to filter by
 * @returns Array of matching node configuration entries
 */
export function getNodeConfigurationsFromTemplates(
	templates: WorkflowMetadata[],
	nodeType: string,
	nodeVersion?: number,
): NodeConfigurationEntry[] {
	const configurations: NodeConfigurationEntry[] = [];

	for (const template of templates) {
		for (const node of template.workflow.nodes) {
			if (node.type !== nodeType) continue;
			if (nodeVersion !== undefined && node.typeVersion !== nodeVersion) continue;

			const config = collectSingleNodeConfiguration(node);
			if (config) {
				configurations.push(config);
			}
		}
	}

	return configurations;
}

/**
 * Format node configuration examples as markdown with token limit
 * Follows the same pattern as node-details.tool.ts for consistency
 */
export function formatNodeConfigurationExamples(
	nodeType: string,
	configurations: NodeConfigurationEntry[],
	nodeVersion?: number,
	maxExamples: number = 1,
	maxChars: number = MAX_NODE_EXAMPLE_CHARS,
): string {
	// Filter by version if specified
	const filtered = nodeVersion
		? configurations.filter((c) => c.version === nodeVersion)
		: configurations;

	if (filtered.length === 0) {
		return `## Node Configuration Examples: ${nodeType}\n\nNo examples found.`;
	}

	// Limit to maxExamples and accumulate within token limit
	const limited = filtered.slice(0, maxExamples);
	const { parts } = limited.reduce<{ parts: string[]; chars: number }>(
		(acc, config) => {
			const exampleStr = JSON.stringify(config.parameters, null, 2);
			if (acc.chars + exampleStr.length <= maxChars) {
				acc.parts.push(
					`### Example (version ${config.version})`,
					'',
					'```json',
					exampleStr,
					'```',
					'',
				);
				acc.chars += exampleStr.length;
			}
			return acc;
		},
		{ parts: [], chars: 0 },
	);

	return [`## Node Configuration Examples: ${nodeType}`, '', ...parts].join('\n');
}
