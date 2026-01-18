"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/SharePoint/descriptions/list/List.resource.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/SharePoint 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./get.operation、./getAll.operation、../helpers/utils。导出:description。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/SharePoint/descriptions/list/List.resource.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/SharePoint/descriptions/list/List_resource.py

import type { INodeProperties } from 'n8n-workflow';

import * as get from './get.operation';
import * as getAll from './getAll.operation';
import { handleErrorPostReceive, simplifyListPostReceive } from '../../helpers/utils';

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['list'],
			},
		},
		options: [
			{
				name: 'Get',
				value: 'get',
				description: 'Retrieve details of a single list',
				routing: {
					request: {
						ignoreHttpStatusErrors: true,
						method: 'GET',
						url: '=/sites/{{ $parameter["site"] }}/lists/{{ $parameter["list"] }}',
					},
					output: {
						postReceive: [handleErrorPostReceive, simplifyListPostReceive],
					},
				},
				action: 'Get list',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Retrieve a list of lists',
				routing: {
					request: {
						method: 'GET',
						url: '=/sites/{{ $parameter["site"] }}/lists',
					},
					output: {
						postReceive: [
							handleErrorPostReceive,
							{
								type: 'rootProperty',
								properties: {
									property: 'value',
								},
							},
							simplifyListPostReceive,
						],
					},
				},
				action: 'Get many lists',
			},
		],
		default: 'getAll',
	},

	...get.description,
	...getAll.description,
];
