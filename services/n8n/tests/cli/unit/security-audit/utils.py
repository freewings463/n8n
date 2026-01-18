"""
MIGRATION-META:
  source_path: packages/cli/src/security-audit/utils.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/security-audit 的模块。导入/依赖:外部:无；内部:n8n-workflow、@/security-audit/types；本地:无。导出:toFlaggedNode、toReportTitle、getNodeTypes。关键函数/方法:toFlaggedNode、toReportTitle、getNodeTypes。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/security-audit/utils.ts -> services/n8n/tests/cli/unit/security-audit/utils.py

import type { IWorkflowBase } from 'n8n-workflow';

import type { Risk } from '@/security-audit/types';

type Node = IWorkflowBase['nodes'][number];

export const toFlaggedNode = ({ node, workflow }: { node: Node; workflow: IWorkflowBase }) => ({
	kind: 'node' as const,
	workflowId: workflow.id,
	workflowName: workflow.name,
	nodeId: node.id,
	nodeName: node.name,
	nodeType: node.type,
});

export const toReportTitle = (riskCategory: Risk.Category) =>
	riskCategory.charAt(0).toUpperCase() + riskCategory.slice(1) + ' Risk Report';

export function getNodeTypes(workflows: IWorkflowBase[], test: (element: Node) => boolean) {
	return workflows.reduce<Risk.NodeLocation[]>((acc, workflow) => {
		workflow.nodes.forEach((node) => {
			if (test(node)) acc.push(toFlaggedNode({ node, workflow }));
		});

		return acc;
	}, []);
}
