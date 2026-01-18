"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/validation/checks/from-ai.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/validation/checks 的工作流校验。导入/依赖:外部:无；内部:n8n-workflow、@/types、@/validation/…/node-type-map；本地:../types、../utils/is-tool。导出:validateFromAi。关键函数/方法:containsFromAi、parametersContainFromAi、validateFromAi。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/validation/checks/from-ai.ts -> services/n8n/tests/n8n-ai-workflow-builder-ee/unit/validation/checks/from_ai.py

import type { INodeTypeDescription, INodeParameters } from 'n8n-workflow';

import type { SimpleWorkflow } from '@/types';
import { createNodeTypeMaps, getNodeTypeForNode } from '@/validation/utils/node-type-map';

import type { ProgrammaticViolation } from '../types';
import { isTool } from '../utils/is-tool';

function containsFromAi(value: unknown): boolean {
	if (typeof value !== 'string') {
		return false;
	}

	return /\$from[Aa][Ii]\(.+\)/.test(value);
}

function parametersContainFromAi(parameters: INodeParameters): boolean {
	for (const value of Object.values(parameters)) {
		if (containsFromAi(value)) {
			return true;
		}

		if (value && typeof value === 'object' && !Array.isArray(value)) {
			if (parametersContainFromAi(value as INodeParameters)) {
				return true;
			}
		}

		if (Array.isArray(value)) {
			for (const item of value) {
				if (containsFromAi(item)) {
					return true;
				}

				if (item && typeof item === 'object' && !Array.isArray(value)) {
					if (parametersContainFromAi(value as INodeParameters)) {
						return true;
					}
				}
			}
		}
	}

	return false;
}

export function validateFromAi(
	workflow: SimpleWorkflow,
	nodeTypes: INodeTypeDescription[],
): ProgrammaticViolation[] {
	const violations: ProgrammaticViolation[] = [];

	if (!workflow.nodes || workflow.nodes.length === 0) {
		return violations;
	}

	const { nodeTypeMap, nodeTypesByName } = createNodeTypeMaps(nodeTypes);

	for (const node of workflow.nodes) {
		const nodeType = getNodeTypeForNode(node, nodeTypeMap, nodeTypesByName);
		if (!nodeType) {
			continue;
		}

		if (isTool(nodeType)) {
			continue;
		}

		if (node.parameters && parametersContainFromAi(node.parameters)) {
			violations.push({
				name: 'non-tool-node-uses-fromai',
				type: 'major',
				description: `Non-tool node "${node.name}" (${node.type}) uses $fromAI in its parameters. $fromAI is only for tool nodes connected to AI agents.`,
				pointsDeducted: 20,
			});
		}
	}

	return violations;
}
