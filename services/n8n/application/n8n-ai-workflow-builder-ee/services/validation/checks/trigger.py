"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/validation/checks/trigger.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/validation/checks 的工作流校验。导入/依赖:外部:无；内部:n8n-workflow、@/types、@/validation/…/node-type-map；本地:../types。导出:TriggerEvaluationResult、validateTrigger。关键函数/方法:isTriggerNode、validateTrigger。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/validation/checks/trigger.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/validation/checks/trigger.py

import type { INodeTypeDescription } from 'n8n-workflow';

import type { SimpleWorkflow } from '@/types';
import { createNodeTypeMaps, getNodeTypeForNode } from '@/validation/utils/node-type-map';

import type { ProgrammaticViolation, SingleEvaluatorResult } from '../types';

export interface TriggerEvaluationResult extends SingleEvaluatorResult {
	hasTrigger: boolean;
	triggerNodes: string[];
}

const isTriggerNode = (nodeType: INodeTypeDescription) => nodeType.group.includes('trigger');

export function validateTrigger(
	workflow: SimpleWorkflow,
	nodeTypes: INodeTypeDescription[],
): ProgrammaticViolation[] {
	const violations: ProgrammaticViolation[] = [];
	const triggerNodes: string[] = [];

	if (!workflow.nodes || workflow.nodes.length === 0) {
		return violations;
	}

	const { nodeTypeMap, nodeTypesByName } = createNodeTypeMaps(nodeTypes);

	for (const node of workflow.nodes) {
		const nodeType = getNodeTypeForNode(node, nodeTypeMap, nodeTypesByName);

		if (!nodeType) {
			continue;
		}

		if (isTriggerNode(nodeType)) {
			triggerNodes.push(node.name);
		}
	}

	const hasTrigger = triggerNodes.length > 0;

	if (!hasTrigger) {
		violations.push({
			name: 'workflow-has-no-trigger',
			type: 'critical',
			description: 'Workflow must have at least one trigger node to start execution',
			pointsDeducted: 50,
		});
	}

	return violations;
}
