"""
MIGRATION-META:
  source_path: packages/cli/src/modules/breaking-changes/rules/v2/removed-nodes.rule.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/breaking-changes/rules 的模块。导入/依赖:外部:无；内部:@n8n/api-types、@n8n/db、@n8n/di、n8n-workflow；本地:../../types。导出:RemovedNodesRule。关键函数/方法:getMetadata、getRecommendations、detectWorkflow。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/breaking-changes/rules/v2/removed-nodes.rule.ts -> services/n8n/application/cli/services/breaking-changes/rules/v2/removed_nodes_rule.py

import type { BreakingChangeAffectedWorkflow, BreakingChangeRecommendation } from '@n8n/api-types';
import type { WorkflowEntity } from '@n8n/db';
import { Service } from '@n8n/di';
import type { INode } from 'n8n-workflow';

import type {
	BreakingChangeRuleMetadata,
	IBreakingChangeWorkflowRule,
	WorkflowDetectionReport,
} from '../../types';
import { BreakingChangeCategory } from '../../types';

@Service()
export class RemovedNodesRule implements IBreakingChangeWorkflowRule {
	private readonly REMOVED_NODES = [
		'n8n-nodes-base.spontit',
		'n8n-nodes-base.crowdDev',
		'n8n-nodes-base.kitemaker',
	];

	id: string = 'removed-nodes-v2';

	getMetadata(): BreakingChangeRuleMetadata {
		return {
			version: 'v2',
			title: 'Removed Deprecated Nodes',
			description: 'Several deprecated nodes have been removed and will no longer work',
			category: BreakingChangeCategory.workflow,
			severity: 'low',
			documentationUrl:
				'https://docs.n8n.io/2-0-breaking-changes/#removed-nodes-for-retired-services',
		};
	}

	async getRecommendations(
		_workflowResults: BreakingChangeAffectedWorkflow[],
	): Promise<BreakingChangeRecommendation[]> {
		return [
			{
				action: 'Update affected workflows',
				description: 'Replace removed nodes with their updated versions or alternatives',
			},
		];
	}

	async detectWorkflow(
		_workflow: WorkflowEntity,
		nodesGroupedByType: Map<string, INode[]>,
	): Promise<WorkflowDetectionReport> {
		const removedNodes = this.REMOVED_NODES.flatMap((type) => nodesGroupedByType.get(type) ?? []);
		if (removedNodes.length === 0) return { isAffected: false, issues: [] };

		return {
			isAffected: true,
			issues: removedNodes.map((node) => ({
				title: `Node '${node.type}' with name '${node.name}' has been removed`,
				description: `The node type '${node.type}' is no longer available. Please replace it with an alternative.`,
				level: 'error',
				nodeId: node.id,
				nodeName: node.name,
			})),
		};
	}
}
