"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Outlook/v2/actions/folder/getAll.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Outlook 的节点。导入/依赖:外部:@utils/utilities；内部:n8n-workflow；本地:../../descriptions、../../transport。导出:properties、description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Outlook/v2/actions/folder/getAll.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Outlook/v2/actions/folder/getAll_operation.py

import type { IDataObject, IExecuteFunctions, INodeProperties } from 'n8n-workflow';

import { updateDisplayOptions } from '@utils/utilities';

import { folderFields, folderRLC, returnAllOrLimit } from '../../descriptions';
import { getSubfolders, microsoftApiRequest, microsoftApiRequestAllItems } from '../../transport';

export const properties: INodeProperties[] = [
	...returnAllOrLimit,
	{
		displayName: 'Filters',
		name: 'filters',
		type: 'collection',
		placeholder: 'Add Filter',
		default: {},
		options: [
			{
				displayName: 'Filter Query',
				name: 'filter',
				type: 'string',
				default: '',
				placeholder: "e.g. displayName eq 'My Folder'",
				hint: 'Search query to filter folders. <a href="https://docs.microsoft.com/en-us/graph/query-parameters#filter-parameter">More info</a>.',
			},
		],
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		options: [
			{
				displayName: 'Fields',
				name: 'fields',
				type: 'multiOptions',
				description: 'The fields to add to the output',
				options: folderFields,
				default: [],
			},
			{
				displayName: 'Include Child Folders',
				name: 'includeChildFolders',
				type: 'boolean',
				default: false,
				description: 'Whether to include child folders in the response',
			},
			{
				...folderRLC,
				displayName: 'Parent Folder',
				required: false,
				description: 'The folder you want to search in',
			},
		],
	},
];

const displayOptions = {
	show: {
		resource: ['folder'],
		operation: ['getAll'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, index: number) {
	let responseData;
	const qs: IDataObject = {};

	const returnAll = this.getNodeParameter('returnAll', index);
	const options = this.getNodeParameter('options', index);
	const filter = this.getNodeParameter('filters.filter', index, '') as string;

	const parentFolderId = this.getNodeParameter('options.folderId', index, '', {
		extractValue: true,
	}) as string;

	if (options.fields) {
		qs.$select = (options.fields as string[]).join(',');
	}

	if (filter) {
		qs.$filter = filter;
	}

	let endpoint;
	if (parentFolderId) {
		endpoint = `/mailFolders/${parentFolderId}/childFolders`;
	} else {
		endpoint = '/mailFolders';
	}

	if (returnAll) {
		responseData = await microsoftApiRequestAllItems.call(this, 'value', 'GET', endpoint, {}, qs);
	} else {
		qs.$top = this.getNodeParameter('limit', index);
		responseData = await microsoftApiRequest.call(this, 'GET', endpoint, {}, qs);
		responseData = responseData.value;
	}

	if (options.includeChildFolders) {
		responseData = await getSubfolders.call(this, responseData as IDataObject[]);
	}

	const executionData = this.helpers.constructExecutionMetaData(
		this.helpers.returnJsonArray(responseData as IDataObject[]),
		{ itemData: { item: index } },
	);

	return executionData;
}
