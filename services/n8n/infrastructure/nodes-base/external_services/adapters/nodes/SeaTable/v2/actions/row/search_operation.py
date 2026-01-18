"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SeaTable/v2/actions/row/search.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SeaTable/v2 的节点。导入/依赖:外部:无；内部:无；本地:../Interfaces。导出:properties、description。关键函数/方法:execute、sqlResult。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SeaTable/v2/actions/row/search.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SeaTable/v2/actions/row/search_operation.py

import {
	type IDataObject,
	type INodeExecutionData,
	type INodeProperties,
	type IExecuteFunctions,
	updateDisplayOptions,
} from 'n8n-workflow';

import {
	seaTableApiRequest,
	enrichColumns,
	simplify_new,
	getBaseCollaborators,
} from '../../GenericFunctions';
import type { IDtableMetadataColumn, IRowResponse } from '../Interfaces';

export const properties: INodeProperties[] = [
	{
		displayName: 'Column Name or ID',
		name: 'searchColumn',
		type: 'options',
		typeOptions: {
			loadOptionsDependsOn: ['tableName'],
			loadOptionsMethod: 'getSearchableColumns',
		},
		required: true,
		default: '',
		// eslint-disable-next-line n8n-nodes-base/node-param-description-wrong-for-dynamic-options
		description:
			'Select the column to be searched. Not all column types are supported for search. Choose from the list, or specify a name using an <a href="https://docs.n8n.io/code-examples/expressions/">expression</a>.',
	},
	{
		displayName: 'Search Term',
		name: 'searchTerm',
		type: 'string',
		required: true,
		default: '',
		description: 'What to look for?',
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add Option',
		default: {},
		options: [
			{
				displayName: 'Case Insensitive Search',
				name: 'insensitive',
				type: 'boolean',
				default: false,
				description:
					'Whether the search ignores case sensitivity (true). Otherwise, it distinguishes between uppercase and lowercase characters.',
			},
			{
				displayName: 'Activate Wildcard Search',
				name: 'wildcard',
				type: 'boolean',
				default: true,
				description:
					'Whether the search only results perfect matches (true). Otherwise, it finds a row even if the search value is part of a string (false).',
			},
			{
				displayName: 'Simplify',
				name: 'simple',
				type: 'boolean',
				default: true,
				description:
					'Whether to return a simplified version of the response instead of the raw data',
			},
			{
				displayName: 'Return Column Names',
				name: 'convert',
				type: 'boolean',
				default: true,
				description: 'Whether to return the column keys (false) or the column names (true)',
			},
		],
	},
];

const displayOptions = {
	show: {
		resource: ['row'],
		operation: ['search'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(
	this: IExecuteFunctions,
	index: number,
): Promise<INodeExecutionData[]> {
	const tableName = this.getNodeParameter('tableName', index) as string;
	const searchColumn = this.getNodeParameter('searchColumn', index) as string;
	const searchTerm = this.getNodeParameter('searchTerm', index) as string | number;
	let searchTermString = String(searchTerm);
	const options = this.getNodeParameter('options', index);

	// get collaborators
	const collaborators = await getBaseCollaborators.call(this);

	// this is the base query. The WHERE has to be finalized...
	let sqlQuery = `SELECT * FROM \`${tableName}\` WHERE \`${searchColumn}\``;

	if (options.insensitive) {
		searchTermString = searchTermString.toLowerCase();
		sqlQuery = `SELECT * FROM \`${tableName}\` WHERE lower(\`${searchColumn}\`)`;
	}

	const wildcard = options.wildcard ?? true;

	if (wildcard) sqlQuery = sqlQuery + ' LIKE "%' + searchTermString + '%"';
	else if (!wildcard) sqlQuery = sqlQuery + ' = "' + searchTermString + '"';

	const sqlResult = (await seaTableApiRequest.call(
		this,
		{},
		'POST',
		'/api-gateway/api/v2/dtables/{{dtable_uuid}}/sql',
		{
			sql: sqlQuery,
			convert_keys: options.convert ?? true,
		},
	)) as IRowResponse;
	const metadata = sqlResult.metadata as IDtableMetadataColumn[];
	const rows = sqlResult.results;

	// hide columns like button
	rows.map((row) => enrichColumns(row, metadata, collaborators));

	// remove columns starting with _;
	if (options.simple) {
		rows.map((row) => simplify_new(row));
	}

	return this.helpers.returnJsonArray(rows as IDataObject[]);
}
