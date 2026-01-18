"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Gong/Gong.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Gong 的节点。导入/依赖:外部:无；内部:无；本地:./descriptions、./GenericFunctions。导出:Gong。关键函数/方法:getCalls、getUsers。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Gong/Gong.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Gong/Gong_node.py

import {
	NodeConnectionTypes,
	type IDataObject,
	type ILoadOptionsFunctions,
	type INodeListSearchItems,
	type INodeListSearchResult,
	type INodeType,
	type INodeTypeDescription,
} from 'n8n-workflow';

import { callFields, callOperations, userFields, userOperations } from './descriptions';
import { gongApiRequest } from './GenericFunctions';

export class Gong implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Gong',
		name: 'gong',
		icon: 'file:gong.svg',
		group: ['transform'],
		version: 1,
		subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
		description: 'Interact with Gong API',
		defaults: {
			name: 'Gong',
		},
		usableAsTool: true,
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'gongApi',
				required: true,
				displayOptions: {
					show: {
						authentication: ['accessToken'],
					},
				},
			},
			{
				name: 'gongOAuth2Api',
				required: true,
				displayOptions: {
					show: {
						authentication: ['oAuth2'],
					},
				},
			},
		],
		requestDefaults: {
			baseURL: '={{ $credentials.baseUrl.replace(new RegExp("/$"), "") }}',
		},
		properties: [
			{
				displayName: 'Authentication',
				name: 'authentication',
				type: 'options',
				options: [
					{
						name: 'Access Token',
						value: 'accessToken',
					},
					{
						name: 'OAuth2',
						value: 'oAuth2',
					},
				],
				default: 'accessToken',
			},
			{
				displayName: 'Resource',
				name: 'resource',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Call',
						value: 'call',
					},
					{
						name: 'User',
						value: 'user',
					},
				],
				default: 'call',
			},
			...callOperations,
			...callFields,
			...userOperations,
			...userFields,
		],
	};

	methods = {
		listSearch: {
			async getCalls(
				this: ILoadOptionsFunctions,
				filter?: string,
				paginationToken?: string,
			): Promise<INodeListSearchResult> {
				const query: IDataObject = {};
				if (paginationToken) {
					query.cursor = paginationToken;
				}

				const responseData = await gongApiRequest.call(this, 'GET', '/v2/calls', {}, query);

				const calls: Array<{
					id: string;
					title: string;
				}> = responseData.calls;

				const results: INodeListSearchItems[] = calls
					.map((c) => ({
						name: c.title,
						value: c.id,
					}))
					.filter(
						(c) =>
							!filter ||
							c.name.toLowerCase().includes(filter.toLowerCase()) ||
							c.value?.toString() === filter,
					)
					.sort((a, b) => {
						if (a.name.toLowerCase() < b.name.toLowerCase()) return -1;
						if (a.name.toLowerCase() > b.name.toLowerCase()) return 1;
						return 0;
					});

				return { results, paginationToken: responseData.records.cursor };
			},

			async getUsers(
				this: ILoadOptionsFunctions,
				filter?: string,
				paginationToken?: string,
			): Promise<INodeListSearchResult> {
				const query: IDataObject = {};
				if (paginationToken) {
					query.cursor = paginationToken;
				}

				const responseData = await gongApiRequest.call(this, 'GET', '/v2/users', {}, query);

				const users: Array<{
					id: string;
					emailAddress: string;
					firstName: string;
					lastName: string;
				}> = responseData.users;

				const results: INodeListSearchItems[] = users
					.map((u) => ({
						name: `${u.firstName} ${u.lastName} (${u.emailAddress})`,
						value: u.id,
					}))
					.filter(
						(u) =>
							!filter ||
							u.name.toLowerCase().includes(filter.toLowerCase()) ||
							u.value?.toString() === filter,
					)
					.sort((a, b) => {
						if (a.name.toLowerCase() < b.name.toLowerCase()) return -1;
						if (a.name.toLowerCase() > b.name.toLowerCase()) return 1;
						return 0;
					});

				return { results, paginationToken: responseData.records.cursor };
			},
		},
	};
}
