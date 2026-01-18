"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/TheHiveProject/actions/query/executeQuery.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/TheHiveProject/actions 的节点。导入/依赖:外部:@utils/utilities；内部:n8n-workflow；本地:../../transport。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/TheHiveProject/actions/query/executeQuery.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/TheHiveProject/actions/query/executeQuery_operation.py

import type {
	IDataObject,
	IExecuteFunctions,
	INodeExecutionData,
	INodeProperties,
} from 'n8n-workflow';
import { NodeOperationError, jsonParse } from 'n8n-workflow';

import { updateDisplayOptions, wrapData } from '@utils/utilities';

import { theHiveApiRequest } from '../../transport';

const properties: INodeProperties[] = [
	{
		displayName: 'Query',
		name: 'queryJson',
		type: 'json',
		required: true,
		default: '=[\n  {\n    "_name": "listOrganisation"\n  }\n]',
		description: 'Search for objects with filtering and sorting capabilities',
		hint: 'The query should be an array of operations with the required selection and optional filtering, sorting, and pagination. See <a href="https://docs.strangebee.com/thehive/api-docs/#operation/Query%20API" target="_blank">Query API</a> for more information.',
		typeOptions: {
			rows: 10,
		},
	},
];

const displayOptions = {
	show: {
		resource: ['query'],
		operation: ['executeQuery'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, i: number): Promise<INodeExecutionData[]> {
	let responseData: IDataObject | IDataObject[] = [];

	const queryJson = this.getNodeParameter('queryJson', i) as string;

	let query: IDataObject = {};
	if (typeof queryJson === 'object') {
		query = queryJson;
	} else {
		query = jsonParse<IDataObject>(queryJson, {
			errorMessage: 'Query JSON must be a valid JSON object',
		});
	}

	if (query.query) {
		query = query.query as IDataObject;
	}

	if (!Array.isArray(query)) {
		throw new NodeOperationError(
			this.getNode(),
			'The query should be an array of operations with the required selection and optional filtering, sorting, and pagination',
		);
	}

	const body: IDataObject = {
		query,
	};

	responseData = await theHiveApiRequest.call(this, 'POST', '/v1/query', body);

	if (typeof responseData !== 'object') {
		responseData = { queryResult: responseData };
	}

	const executionData = this.helpers.constructExecutionMetaData(wrapData(responseData), {
		itemData: { item: i },
	});

	return executionData;
}
