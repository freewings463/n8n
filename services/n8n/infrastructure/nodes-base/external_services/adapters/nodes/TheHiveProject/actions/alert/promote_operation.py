"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/TheHiveProject/actions/alert/promote.operation.ts
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
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/TheHiveProject/actions/alert/promote.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/TheHiveProject/actions/alert/promote_operation.py

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
		placeholder: 'Add Field',
		type: 'collection',
		default: {},
		options: [
			{
				displayName: 'Case Template Name or ID',
				name: 'caseTemplate',
				type: 'options',
				description:
					'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
				default: '',
				typeOptions: {
					loadOptionsMethod: 'loadCaseTemplate',
				},
			},
		],
	},
];

const displayOptions = {
	show: {
		resource: ['alert'],
		operation: ['promote'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, i: number): Promise<INodeExecutionData[]> {
	let responseData: IDataObject | IDataObject[] = [];

	const alertId = this.getNodeParameter('alertId', i, '', { extractValue: true }) as string;
	const caseTemplate = this.getNodeParameter('options.caseTemplate', i, '') as string;

	const body: IDataObject = {};

	// await theHiveApiRequest.call(this, 'POST', '/v1/caseTemplate', {
	// 	name: 'test template 001',
	// 	displayName: 'Test Template 001',
	// 	description: 'test',
	// });

	if (caseTemplate) {
		body.caseTemplate = caseTemplate;
	}

	responseData = await theHiveApiRequest.call(this, 'POST', `/v1/alert/${alertId}/case`, body);

	const executionData = this.helpers.constructExecutionMetaData(wrapData(responseData), {
		itemData: { item: i },
	});

	return executionData;
}
