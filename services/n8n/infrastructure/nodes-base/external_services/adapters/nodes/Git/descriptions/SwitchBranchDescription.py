"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Git/descriptions/SwitchBranchDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Git/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:switchBranchFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Git/descriptions/SwitchBranchDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Git/descriptions/SwitchBranchDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const switchBranchFields: INodeProperties[] = [
	{
		displayName: 'Branch Name',
		name: 'branchName',
		type: 'string',
		displayOptions: {
			show: {
				operation: ['switchBranch'],
			},
		},
		default: '',
		placeholder: 'feature/new-feature',
		required: true,
		description: 'The name of the branch to switch to',
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		displayOptions: {
			show: {
				operation: ['switchBranch'],
			},
		},
		placeholder: 'Add option',
		default: {},
		options: [
			{
				displayName: 'Create Branch If Not Exists',
				name: 'createBranch',
				type: 'boolean',
				default: true,
				description: 'Whether to create the branch if it does not exist',
			},
			{
				displayName: 'Start Point',
				name: 'startPoint',
				type: 'string',
				default: '',
				placeholder: 'main',
				description:
					'The commit/branch/tag to create the new branch from. If not set, creates from current HEAD.',
				displayOptions: {
					show: {
						createBranch: [true],
					},
				},
			},
			{
				displayName: 'Force Switch',
				name: 'force',
				type: 'boolean',
				default: false,
				description: 'Whether to force the branch switch, discarding any local changes',
			},
			{
				displayName: 'Set Upstream',
				name: 'setUpstream',
				type: 'boolean',
				default: false,
				description: 'Whether to set up tracking to a remote branch when creating a new branch',
				displayOptions: {
					show: {
						createBranch: [true],
					},
				},
			},
			{
				displayName: 'Remote Name',
				name: 'remoteName',
				type: 'string',
				default: 'origin',
				placeholder: 'origin',
				description: 'The name of the remote to track',
				displayOptions: {
					show: {
						createBranch: [true],
						setUpstream: [true],
					},
				},
			},
		],
	},
];
