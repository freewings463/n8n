"""
MIGRATION-META:
  source_path: packages/cli/src/modules/breaking-changes/rules/v2/git-node-bare-repos.rule.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/breaking-changes/rules 的模块。导入/依赖:外部:无；内部:@n8n/api-types、@n8n/db、@n8n/di、n8n-workflow；本地:../../types。导出:GitNodeBareReposRule。关键函数/方法:getMetadata、getRecommendations、detectWorkflow。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/breaking-changes/rules/v2/git-node-bare-repos.rule.ts -> services/n8n/application/cli/services/breaking-changes/rules/v2/git_node_bare_repos_rule.py

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
export class GitNodeBareReposRule implements IBreakingChangeWorkflowRule {
	id: string = 'git-node-bare-repos-v2';

	getMetadata(): BreakingChangeRuleMetadata {
		return {
			version: 'v2',
			title: 'Git node bare repositories disabled by default',
			description:
				'N8N_GIT_NODE_DISABLE_BARE_REPOS now defaults to true for security. Bare repositories are disabled to prevent RCE attacks via Git hooks',
			category: BreakingChangeCategory.workflow,
			severity: 'medium',
			documentationUrl:
				'https://docs.n8n.io/2-0-breaking-changes/#change-the-default-value-of-n8n_git_node_disable_bare_repos-to-true',
		};
	}

	async getRecommendations(
		_workflowResults: BreakingChangeAffectedWorkflow[],
	): Promise<BreakingChangeRecommendation[]> {
		return [
			{
				action: 'Review Git node usage',
				description:
					'Check if any Git nodes in your workflows use bare repositories. Bare repositories are now disabled by default for security reasons.',
			},
			{
				action: 'Migrate away from bare repositories',
				description:
					'If possible, update your workflows to use regular Git repositories instead of bare repositories.',
			},
			{
				action: 'Enable bare repositories if required (not recommended)',
				description:
					'If you absolutely need bare repository support and understand the security risks, set N8N_GIT_NODE_DISABLE_BARE_REPOS=false. This is not recommended as it exposes your instance to potential RCE attacks via Git hooks.',
			},
		];
	}

	async detectWorkflow(
		_workflow: WorkflowEntity,
		nodesGroupedByType: Map<string, INode[]>,
	): Promise<WorkflowDetectionReport> {
		// Check if N8N_GIT_NODE_DISABLE_BARE_REPOS is already set to false
		// If it's explicitly set to false, the user has opted in to allow bare repos
		const disableBareRepos = process.env.N8N_GIT_NODE_DISABLE_BARE_REPOS;
		if (disableBareRepos === 'false') {
			// User has explicitly enabled bare repos, so they're aware of the change
			return { isAffected: false, issues: [] };
		}

		// Check if the workflow contains Git nodes
		const gitNodes = nodesGroupedByType.get('n8n-nodes-base.git') ?? [];

		if (gitNodes.length === 0) {
			return { isAffected: false, issues: [] };
		}

		// We can't easily detect if a Git node is using a bare repository from the parameters
		// So we flag all Git nodes as potentially affected for user review
		return {
			isAffected: true,
			issues: gitNodes.map((node) => ({
				title: `Git node '${node.name}' may be affected by bare repository restrictions`,
				description:
					'This workflow contains a Git node. Bare repositories are now disabled by default for security reasons. If this node uses bare repositories, it may fail. Review your Git node configuration and migrate to regular repositories if needed, or set N8N_GIT_NODE_DISABLE_BARE_REPOS=false (not recommended) to re-enable bare repository support.',
				level: 'warning',
				nodeId: node.id,
				nodeName: node.name,
			})),
		};
	}
}
