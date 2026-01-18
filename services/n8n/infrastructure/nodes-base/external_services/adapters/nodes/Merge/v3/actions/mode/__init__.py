"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Merge/v3/actions/mode/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Merge/v3 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./append、./chooseBranch、./combineAll、./combineByFields 等2项。导出:append、chooseBranch、combineAll、combineByFields、combineBySql、combineByPosition、description。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Merge/v3/actions/mode/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Merge/v3/actions/mode/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as append from './append';
import * as chooseBranch from './chooseBranch';
import * as combineAll from './combineAll';
import * as combineByFields from './combineByFields';
import * as combineByPosition from './combineByPosition';
import * as combineBySql from './combineBySql';

export { append, chooseBranch, combineAll, combineByFields, combineBySql, combineByPosition };

export const description: INodeProperties[] = [
	{
		displayName: 'Mode',
		name: 'mode',
		type: 'options',
		noDataExpression: true,
		options: [
			{
				name: 'Append',
				value: 'append',
				description: 'Output items of each input, one after the other',
			},
			{
				name: 'Combine',
				value: 'combine',
				description: 'Merge matching items together',
			},
			{
				name: 'SQL Query',
				value: 'combineBySql',
				description: 'Write a query to do the merge',
			},
			{
				name: 'Choose Branch',
				value: 'chooseBranch',
				description: 'Output data from a specific branch, without modifying it',
			},
		],
		default: 'append',
		description: 'How input data should be merged',
	},
	{
		displayName: 'Combine By',
		name: 'combineBy',
		type: 'options',
		noDataExpression: true,
		options: [
			{
				name: 'Matching Fields',
				value: 'combineByFields',
				description: 'Combine items with the same field values',
			},
			{
				name: 'Position',
				value: 'combineByPosition',
				description: 'Combine items based on their order',
			},
			{
				name: 'All Possible Combinations',
				value: 'combineAll',
				description: 'Every pairing of every two items (cross join)',
			},
		],
		default: 'combineByFields',
		description: 'How input data should be merged',
		displayOptions: {
			show: { mode: ['combine'] },
		},
	},
	...append.description,
	...combineAll.description,
	...combineByFields.description,
	...combineBySql.description,
	...combineByPosition.description,
	...chooseBranch.description,
];
