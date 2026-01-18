"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/template/templates/declarative/github-issues/template/nodes/GithubIssues/resources/issue/get.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/template/templates/declarative 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../shared/descriptions。导出:issueGetDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - node-cli templates -> infrastructure/configuration/tooling/templates
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/template/templates/declarative/github-issues/template/nodes/GithubIssues/resources/issue/get.ts -> services/n8n/infrastructure/n8n-node-cli/configuration/tooling/templates/templates/declarative/github-issues/template/nodes/GithubIssues/resources/issue/get.py

import type { INodeProperties } from 'n8n-workflow';
import { issueSelect } from '../../shared/descriptions';

const showOnlyForIssueGet = {
	operation: ['get'],
	resource: ['issue'],
};

export const issueGetDescription: INodeProperties[] = [
	{
		...issueSelect,
		displayOptions: { show: showOnlyForIssueGet },
	},
];
