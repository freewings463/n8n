"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Git/descriptions/CommitDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Git/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:commitFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Git/descriptions/CommitDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Git/descriptions/CommitDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const commitFields: INodeProperties[] = [
	{
		displayName: 'Message',
		name: 'message',
		type: 'string',
		displayOptions: {
			show: {
				operation: ['commit'],
			},
		},
		default: '',
		description: 'The commit message to use',
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		displayOptions: {
			show: {
				operation: ['commit'],
			},
		},
		placeholder: 'Add option',
		default: {},
		options: [
			{
				displayName: 'Branch',
				name: 'branch',
				type: 'string',
				default: '',
				placeholder: 'main',
				description:
					'The branch to switch to before committing. If empty or not set, will commit to current branch.',
			},
			{
				displayName: 'Paths to Add',
				name: 'pathsToAdd',
				type: 'string',
				default: '',
				placeholder: '/data/file1.json',
				description:
					'Comma-separated list of paths (absolute or relative to Repository Path) of files or folders to commit. If not set will all "added" files and folders be committed.',
			},
		],
	},
];
