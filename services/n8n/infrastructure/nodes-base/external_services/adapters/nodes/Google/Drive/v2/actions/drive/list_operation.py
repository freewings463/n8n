"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Drive/v2/actions/drive/list.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Drive 的节点。导入/依赖:外部:@utils/utilities；内部:无；本地:../../transport。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Drive/v2/actions/drive/list.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Drive/v2/actions/drive/list_operation.py

import type {
	IExecuteFunctions,
	IDataObject,
	INodeExecutionData,
	INodeProperties,
} from 'n8n-workflow';

import { updateDisplayOptions } from '@utils/utilities';

import { googleApiRequest, googleApiRequestAllItems } from '../../transport';

const properties: INodeProperties[] = [
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		displayOptions: {
			show: {
				returnAll: [false],
			},
		},
		typeOptions: {
			minValue: 1,
			maxValue: 200,
		},
		default: 100,
		description: 'Max number of results to return',
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add option',
		default: {},
		options: [
			{
				displayName: 'Query',
				name: 'q',
				type: 'string',
				default: '',
				description:
					'Query string for searching shared drives. See the <a href="https://developers.google.com/drive/api/v3/search-shareddrives">"Search for shared drives"</a> guide for supported syntax.',
			},
			{
				displayName: 'Use Domain Admin Access',
				name: 'useDomainAdminAccess',
				type: 'boolean',
				default: false,
				description:
					'Whether to issue the request as a domain administrator; if set to true, then the requester will be granted access if they are an administrator of the domain to which the shared drive belongs',
			},
		],
	},
];

const displayOptions = {
	show: {
		resource: ['drive'],
		operation: ['list'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, i: number): Promise<INodeExecutionData[]> {
	const returnData: INodeExecutionData[] = [];
	const options = this.getNodeParameter('options', i);

	const returnAll = this.getNodeParameter('returnAll', i);

	const qs: IDataObject = {};

	let response: IDataObject[] = [];

	Object.assign(qs, options);

	if (returnAll) {
		response = await googleApiRequestAllItems.call(
			this,
			'GET',
			'drives',
			'/drive/v3/drives',
			{},
			qs,
		);
	} else {
		qs.pageSize = this.getNodeParameter('limit', i);
		const data = await googleApiRequest.call(this, 'GET', '/drive/v3/drives', {}, qs);
		response = data.drives as IDataObject[];
	}

	const executionData = this.helpers.constructExecutionMetaData(
		this.helpers.returnJsonArray(response),
		{ itemData: { item: i } },
	);

	returnData.push(...executionData);

	return returnData;
}
