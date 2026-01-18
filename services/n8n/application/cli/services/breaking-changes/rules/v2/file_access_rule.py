"""
MIGRATION-META:
  source_path: packages/cli/src/modules/breaking-changes/rules/v2/file-access.rule.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/breaking-changes/rules 的模块。导入/依赖:外部:无；内部:@n8n/api-types、@n8n/db、@n8n/di、n8n-workflow；本地:../../types。导出:FileAccessRule。关键函数/方法:getMetadata、getRecommendations、detectWorkflow。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/breaking-changes/rules/v2/file-access.rule.ts -> services/n8n/application/cli/services/breaking-changes/rules/v2/file_access_rule.py

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
export class FileAccessRule implements IBreakingChangeWorkflowRule {
	private readonly FILE_NODES = ['n8n-nodes-base.readWriteFile', 'n8n-nodes-base.readBinaryFiles'];

	id: string = 'file-access-restriction-v2';

	getMetadata(): BreakingChangeRuleMetadata {
		return {
			version: 'v2',
			title: 'File Access Restrictions',
			description: 'File access is now restricted to a default directory for security purposes',
			category: BreakingChangeCategory.workflow,
			severity: 'medium',
			documentationUrl:
				'https://docs.n8n.io/2-0-breaking-changes/#set-default-value-for-n8n_restrict_file_access_to',
		};
	}

	async getRecommendations(
		_workflowResults: BreakingChangeAffectedWorkflow[],
	): Promise<BreakingChangeRecommendation[]> {
		return [
			{
				action: 'Configure file access paths',
				description:
					'Set N8N_RESTRICT_FILE_ACCESS_TO to a semicolon-separated list of allowed paths if workflows need to access files outside the default directory',
			},
		];
	}

	async detectWorkflow(
		_workflow: WorkflowEntity,
		nodesGroupedByType: Map<string, INode[]>,
	): Promise<WorkflowDetectionReport> {
		const fileNodes = this.FILE_NODES.flatMap((nodeType) => nodesGroupedByType.get(nodeType) ?? []);
		if (fileNodes.length === 0) return { isAffected: false, issues: [] };

		return {
			isAffected: true,
			issues: fileNodes.map((node) => ({
				title: `File access node '${node.type}' with name '${node.name}' affected`,
				description: 'File access for this node is now restricted to configured directories.',
				level: 'warning',
				nodeId: node.id,
				nodeName: node.name,
			})),
		};
	}
}
