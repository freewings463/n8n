"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtop/actions/file/getMany.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtop/actions 的节点。导入/依赖:外部:无；内部:无；本地:./helpers、../utils/utilities、../../transport、../transport/types。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtop/actions/file/getMany.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtop/actions/file/getMany_operation.py

import {
	type IExecuteFunctions,
	type INodeExecutionData,
	type INodeProperties,
} from 'n8n-workflow';

import { requestAllFiles } from './helpers';
import { wrapData } from '../../../../utils/utilities';
import { apiRequest } from '../../transport';
import type { IAirtopResponse } from '../../transport/types';

const displayOptions = {
	show: {
		resource: ['file'],
		operation: ['getMany'],
	},
};

export const description: INodeProperties[] = [
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		displayOptions,
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		displayOptions: {
			show: {
				resource: ['file'],
				operation: ['getMany'],
				returnAll: [false],
			},
		},
		typeOptions: {
			minValue: 1,
			maxValue: 100,
		},
		default: 10,
		description: 'Max number of results to return',
	},
	{
		displayName: 'Session IDs',
		name: 'sessionIds',
		type: 'string',
		default: '',
		description:
			'Comma-separated list of <a href="https://docs.airtop.ai/api-reference/airtop-api/sessions/create" target="_blank">Session IDs</a> to filter files by. When empty, all files from all sessions will be returned.',
		placeholder: 'e.g. 6aac6f73-bd89-4a76-ab32-5a6c422e8b0b, a13c6f73-bd89-4a76-ab32-5a6c422e8224',
		displayOptions,
	},
	{
		displayName: 'Output Files in Single Item',
		name: 'outputSingleItem',
		type: 'boolean',
		default: true,
		description:
			'Whether to output one item containing all files or output each file as a separate item',
		displayOptions,
	},
];

export async function execute(
	this: IExecuteFunctions,
	index: number,
): Promise<INodeExecutionData[]> {
	const returnAll = this.getNodeParameter('returnAll', index, false);
	const limit = this.getNodeParameter('limit', index, 10);
	const sessionIds = this.getNodeParameter('sessionIds', index, '') as string;
	const outputSingleItem = this.getNodeParameter('outputSingleItem', index, true) as boolean;

	const endpoint = '/files';
	let files: IAirtopResponse[] = [];

	const responseData = returnAll
		? await requestAllFiles.call(this, sessionIds)
		: await apiRequest.call(this, 'GET', endpoint, {}, { sessionIds, limit });

	if (responseData.data?.files && Array.isArray(responseData.data?.files)) {
		files = responseData.data.files;
	}

	/**
	 * Returns the files in one of two formats:
	 * - A single JSON item containing an array of all files (when outputSingleItem = true)
	 * - Multiple JSON items, one per file
	 * Data structure reference: https://docs.n8n.io/courses/level-two/chapter-1/#data-structure-of-n8n
	 */
	if (outputSingleItem) {
		return this.helpers.returnJsonArray({ ...responseData });
	}
	return wrapData(files);
}
