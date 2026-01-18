"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtable/v2/actions/base/getMany.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtable/v2 的节点。导入/依赖:外部:无；内部:无；本地:../../transport。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtable/v2/actions/base/getMany.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtable/v2/actions/base/getMany_operation.py

import type {
	IDataObject,
	INodeExecutionData,
	INodeProperties,
	IExecuteFunctions,
} from 'n8n-workflow';

import {
	generatePairedItemData,
	updateDisplayOptions,
	wrapData,
} from '../../../../../utils/utilities';
import { apiRequest } from '../../transport';

const properties: INodeProperties[] = [
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: true,
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
			maxValue: 100,
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
				displayName: 'Permission Level',
				name: 'permissionLevel',
				type: 'multiOptions',
				options: [
					{
						name: 'Comment',
						value: 'comment',
					},
					{
						name: 'Create',
						value: 'create',
					},
					{
						name: 'Edit',
						value: 'edit',
					},
					{
						name: 'None',
						value: 'none',
					},
					{
						name: 'Read',
						value: 'read',
					},
				],
				default: [],
				description: 'Filter the returned bases by one or more permission levels',
			},
		],
	},
];

const displayOptions = {
	show: {
		resource: ['base'],
		operation: ['getMany'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions): Promise<INodeExecutionData[]> {
	const returnAll = this.getNodeParameter('returnAll', 0);

	const endpoint = 'meta/bases';
	let bases: IDataObject[] = [];

	if (returnAll) {
		let offset: string | undefined = undefined;
		do {
			const responseData = await apiRequest.call(this, 'GET', endpoint);
			bases.push(...(responseData.bases as IDataObject[]));
			offset = responseData.offset;
		} while (offset);
	} else {
		const responseData = await apiRequest.call(this, 'GET', endpoint);

		const limit = this.getNodeParameter('limit', 0);
		if (limit && responseData.bases?.length) {
			bases = responseData.bases.slice(0, limit);
		}
	}

	const permissionLevel = this.getNodeParameter('options.permissionLevel', 0, []) as string[];
	if (permissionLevel.length) {
		bases = bases.filter((base) => permissionLevel.includes(base.permissionLevel as string));
	}

	const itemData = generatePairedItemData(this.getInputData().length);

	const returnData = this.helpers.constructExecutionMetaData(wrapData(bases), {
		itemData,
	});

	return returnData;
}
