"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/validation/checks/connections.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/validation/checks 的工作流校验。导入/依赖:外部:无；内部:n8n-workflow、@/types、@/utils/node-helpers、@/validation/…/node-type-map、@/validation/…/resolve-connections；本地:无。导出:validateConnections。关键函数/方法:getProvidedInputTypes、checkMissingRequiredInputs、checkUnsupportedConnections、checkMergeNodeConnections、checkSubNodeRootConnections、validateConnections。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/validation/checks/connections.ts -> services/n8n/tests/n8n-ai-workflow-builder-ee/unit/validation/checks/connections.py

import type { INodeConnections, INodeTypeDescription, NodeConnectionType } from 'n8n-workflow';
import { mapConnectionsByDestination } from 'n8n-workflow';

import type { SimpleWorkflow } from '@/types';
import { isSubNode } from '@/utils/node-helpers';
import { createNodeTypeMaps, getNodeTypeForNode } from '@/validation/utils/node-type-map';
import { resolveNodeInputs, resolveNodeOutputs } from '@/validation/utils/resolve-connections';

import type {
	NodeResolvedConnectionTypesInfo,
	ProgrammaticViolation,
	SingleEvaluatorResult,
} from '../types';

function getProvidedInputTypes(
	nodeConnections?: INodeConnections,
): Map<NodeConnectionType, number> {
	const providedInputTypes = new Map<NodeConnectionType, number>();

	if (!nodeConnections) return providedInputTypes;

	for (const [connectionType, connections] of Object.entries(nodeConnections)) {
		let totalConnections = 0;
		for (const connectionSet of connections) {
			if (!connectionSet) continue;
			totalConnections += connectionSet.length;
		}
		if (totalConnections > 0) {
			providedInputTypes.set(connectionType as NodeConnectionType, totalConnections);
		}
	}

	return providedInputTypes;
}

function checkMissingRequiredInputs(
	nodeInfo: NodeResolvedConnectionTypesInfo,
	providedInputTypes: Map<NodeConnectionType, number>,
): SingleEvaluatorResult['violations'] {
	const issues: SingleEvaluatorResult['violations'] = [];

	if (!nodeInfo.resolvedInputs) return issues;

	for (const input of nodeInfo.resolvedInputs) {
		const providedCount = providedInputTypes.get(input.type) ?? 0;

		if (input.required && providedCount === 0) {
			issues.push({
				name: 'node-missing-required-input',
				type: 'critical',
				description: `Node ${nodeInfo.node.name} (${nodeInfo.node.type}) is missing required input of type ${input.type}`,
				pointsDeducted: 50,
			});
		}
	}

	return issues;
}

function checkUnsupportedConnections(
	nodeInfo: NodeResolvedConnectionTypesInfo,
	providedInputTypes: Map<NodeConnectionType, number>,
): SingleEvaluatorResult['violations'] {
	const issues: SingleEvaluatorResult['violations'] = [];

	if (!nodeInfo.resolvedInputs) return issues;

	const supportedTypes = new Set(nodeInfo.resolvedInputs.map((input) => input.type));
	for (const [type] of providedInputTypes) {
		if (!supportedTypes.has(type)) {
			issues.push({
				name: 'node-unsupported-connection-input',
				type: 'critical',
				description: `Node ${nodeInfo.node.name} (${nodeInfo.node.type}) received unsupported connection type ${type}`,
				pointsDeducted: 50,
			});
		}
	}

	return issues;
}

function checkMergeNodeConnections(
	nodeInfo: NodeResolvedConnectionTypesInfo,
	nodeConnections?: INodeConnections,
): SingleEvaluatorResult['violations'] {
	const issues: SingleEvaluatorResult['violations'] = [];

	if (/\.merge$/.test(nodeInfo.node.type)) {
		// Merge node's number of inputs is controlled by the numberInputs parameter (default 2)
		// The node type definition has static inputs, so we must read from parameters directly
		const numberInputsParam = nodeInfo.node.parameters?.numberInputs;
		const expectedInputs = typeof numberInputsParam === 'number' ? numberInputsParam : 2;

		const mainConnections = nodeConnections?.main ?? [];

		// Count actual input slots that have connections (not total connections)
		const connectedSlots = mainConnections.filter(
			(slot) => Array.isArray(slot) && slot.length > 0,
		).length;

		if (connectedSlots < 2) {
			issues.push({
				name: 'node-merge-single-input',
				type: 'major',
				description: `Merge node ${nodeInfo.node.name} has only ${connectedSlots} input connection(s). Merge nodes require at least 2 inputs to function properly.`,
				pointsDeducted: 20,
			});
		}

		// Check if all expected input slots have connections
		const missingIndexes: number[] = [];

		for (let inputIndex = 0; inputIndex < expectedInputs; inputIndex++) {
			const connectionsForIndex = mainConnections[inputIndex];
			const hasConnections = Array.isArray(connectionsForIndex) && connectionsForIndex.length > 0;

			if (!hasConnections) {
				missingIndexes.push(inputIndex + 1);
			}
		}

		if (missingIndexes.length > 0) {
			issues.push({
				name: 'node-merge-missing-input',
				type: 'major',
				description: `Merge node ${nodeInfo.node.name} is missing connections for input(s) ${missingIndexes.join(', ')}.`,
				pointsDeducted: 20,
			});
		}
	}

	return issues;
}

function checkSubNodeRootConnections(
	workflow: SimpleWorkflow,
	nodeInfo: NodeResolvedConnectionTypesInfo,
	nodesByName: Map<string, SimpleWorkflow['nodes'][number]>,
): ProgrammaticViolation[] {
	const issues: ProgrammaticViolation[] = [];

	const { node, nodeType, resolvedOutputs } = nodeInfo;

	if (!resolvedOutputs || resolvedOutputs.size === 0) {
		return issues;
	}

	if (!isSubNode(nodeType, node)) {
		return issues;
	}

	const aiOutputs = Array.from(resolvedOutputs).filter((output) => output.startsWith('ai_'));

	if (aiOutputs.length === 0) {
		return issues;
	}

	const nodeConnections = workflow.connections?.[node.name];

	for (const outputType of aiOutputs) {
		const connectionsForType = nodeConnections?.[outputType];

		const hasRootConnection = connectionsForType?.some((connectionGroup) =>
			connectionGroup?.some((connection) => connection?.node && nodesByName.has(connection.node)),
		);

		if (!hasRootConnection) {
			issues.push({
				name: 'sub-node-not-connected',
				type: 'critical',
				description: `Sub-node ${node.name} (${node.type}) provides ${outputType} but is not connected to a root node.`,
				pointsDeducted: 50,
			});
		}
	}

	return issues;
}

export function validateConnections(
	workflow: SimpleWorkflow,
	nodeTypes: INodeTypeDescription[],
): ProgrammaticViolation[] {
	const violations: SingleEvaluatorResult['violations'] = [];

	if (!workflow.connections) {
		workflow.connections = {};
	}

	const connectionsByDestination = mapConnectionsByDestination(workflow.connections);
	const nodesByName = new Map(workflow.nodes.map((node) => [node.name, node]));
	const { nodeTypeMap, nodeTypesByName } = createNodeTypeMaps(nodeTypes);

	for (const node of workflow.nodes) {
		const nodeType = getNodeTypeForNode(node, nodeTypeMap, nodeTypesByName);
		if (!nodeType) {
			violations.push({
				name: 'node-type-not-found',
				type: 'critical',
				description: `Node type ${node.type} not found for node ${node.name}`,
				pointsDeducted: 50,
			});
			continue;
		}

		const nodeInfo: NodeResolvedConnectionTypesInfo = { node, nodeType };

		try {
			nodeInfo.resolvedInputs = resolveNodeInputs(nodeInfo);
			nodeInfo.resolvedOutputs = resolveNodeOutputs(nodeInfo);
		} catch (error) {
			violations.push({
				name: 'failed-to-resolve-connections',
				type: 'critical',
				description: `Failed to resolve connections for node ${node.name} (${node.type}): ${
					error instanceof Error ? error.message : String(error)
				}`,
				pointsDeducted: 50,
			});

			continue;
		}

		const nodeConnections = connectionsByDestination[node.name];
		const providedInputTypes = getProvidedInputTypes(nodeConnections);

		violations.push(...checkMissingRequiredInputs(nodeInfo, providedInputTypes));

		violations.push(...checkUnsupportedConnections(nodeInfo, providedInputTypes));

		violations.push(...checkMergeNodeConnections(nodeInfo, nodeConnections));

		violations.push(...checkSubNodeRootConnections(workflow, nodeInfo, nodesByName));
	}

	return violations;
}
