"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Splunk/v2/actions/search/getAll.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Splunk/v2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../utils/utilities、../helpers/utils、../../transport。导出:description。关键函数/方法:execute、populate。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Splunk/v2/actions/search/getAll.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Splunk/v2/actions/search/getAll_operation.py

import type { INodeProperties, IExecuteFunctions, IDataObject } from 'n8n-workflow';

import { updateDisplayOptions } from '../../../../../utils/utilities';
import { populate, setReturnAllOrLimit } from '../../helpers/utils';
import { splunkApiJsonRequest } from '../../transport';

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
		default: 50,
		description: 'Max number of results to return',
		typeOptions: {
			minValue: 1,
		},
		displayOptions: {
			show: {
				returnAll: [false],
			},
		},
	},
	{
		displayName: 'Sort',
		name: 'sort',
		type: 'fixedCollection',
		default: {},
		options: [
			{
				displayName: 'Values',
				name: 'values',
				values: [
					{
						displayName: 'Sort Direction',
						name: 'sort_dir',
						type: 'options',
						options: [
							{
								name: 'Ascending',
								value: 'asc',
							},
							{
								name: 'Descending',
								value: 'desc',
							},
						],
						default: 'asc',
					},
					{
						displayName: 'Sort Key',
						name: 'sort_key',
						description: 'Key name to use for sorting',
						type: 'string',
						placeholder: 'e.g. diskUsage',
						default: '',
					},
					{
						displayName: 'Sort Mode',
						name: 'sort_mode',
						type: 'options',
						options: [
							{
								name: 'Automatic',
								value: 'auto',
								description:
									'If all field values are numeric, collate numerically. Otherwise, collate alphabetically.',
							},
							{
								name: 'Alphabetic',
								value: 'alpha',
								description: 'Collate alphabetically, case-insensitive',
							},
							{
								name: 'Alphabetic and Case-Sensitive',
								value: 'alpha_case',
								description: 'Collate alphabetically, case-sensitive',
							},
							{
								name: 'Numeric',
								value: 'num',
								description: 'Collate numerically',
							},
						],
						default: 'auto',
					},
				],
			},
		],
	},
];

const displayOptions = {
	show: {
		resource: ['search'],
		operation: ['getAll'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(
	this: IExecuteFunctions,
	i: number,
): Promise<IDataObject | IDataObject[]> {
	// https://docs.splunk.com/Documentation/Splunk/8.2.2/RESTREF/RESTsearch#search.2Fjobs

	const qs = {} as IDataObject;
	const sort = this.getNodeParameter('sort.values', i, {}) as IDataObject;

	populate(sort, qs);
	setReturnAllOrLimit.call(this, qs);

	const endpoint = '/services/search/jobs';
	const returnData = await splunkApiJsonRequest.call(this, 'GET', endpoint, {}, qs);

	return returnData;
}
