"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/TheHiveProject/actions/alert/get.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/TheHiveProject/actions 的节点。导入/依赖:外部:@utils/utilities；内部:无；本地:../../descriptions、../../transport。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/TheHiveProject/actions/alert/get.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/TheHiveProject/actions/alert/get_operation.py

import type {
	IDataObject,
	IExecuteFunctions,
	INodeExecutionData,
	INodeProperties,
} from 'n8n-workflow';

import { updateDisplayOptions, wrapData } from '@utils/utilities';

import { alertRLC } from '../../descriptions';
import { theHiveApiRequest } from '../../transport';

const properties: INodeProperties[] = [
	alertRLC,
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add option',
		default: {},
		options: [
			{
				displayName: 'Include Similar Alerts',
				name: 'includeSimilarAlerts',
				type: 'boolean',
				description: 'Whether to include similar cases',
				default: false,
			},
			{
				displayName: 'Include Similar Cases',
				name: 'includeSimilarCases',
				type: 'boolean',
				description: 'Whether to include similar cases',
				default: false,
			},
		],
	},
];

const displayOptions = {
	show: {
		resource: ['alert'],
		operation: ['get'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, i: number): Promise<INodeExecutionData[]> {
	let responseData: IDataObject;

	const alertId = this.getNodeParameter('alertId', i, '', { extractValue: true }) as string;
	const options = this.getNodeParameter('options', i, {});

	responseData = await theHiveApiRequest.call(this, 'GET', `/v1/alert/${alertId}`);

	if (responseData && options.includeSimilarAlerts) {
		const similarAlerts = await theHiveApiRequest.call(this, 'POST', '/v1/query', {
			query: [
				{
					_name: 'getAlert',
					idOrName: alertId,
				},
				{
					_name: 'similarAlerts',
				},
			],
		});

		responseData = {
			...responseData,
			similarAlerts,
		};
	}

	if (responseData && options.includeSimilarCases) {
		const similarCases = await theHiveApiRequest.call(this, 'POST', '/v1/query', {
			query: [
				{
					_name: 'getAlert',
					idOrName: alertId,
				},
				{
					_name: 'similarCases',
				},
			],
		});

		responseData = {
			...responseData,
			similarCases,
		};
	}

	const executionData = this.helpers.constructExecutionMetaData(wrapData(responseData), {
		itemData: { item: i },
	});

	return executionData;
}
