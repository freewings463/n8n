"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SeaTable/v2/methods/loadOptions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SeaTable/v2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../actions/Interfaces、../GenericFunctions。导出:无。关键函数/方法:getTableNames、getTableNameAndId、getSearchableColumns、getLinkColumns、getLinkColumnsWithColumnKey、getAssetColumns、getSignatureColumns、getTableUpdateAbleColumns、getRowIds、getTableViews。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SeaTable/v2/methods/loadOptions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SeaTable/v2/methods/loadOptions.py

import type { ILoadOptionsFunctions, INodePropertyOptions } from 'n8n-workflow';

import type { IRow } from '../actions/Interfaces';
import { getTableColumns, seaTableApiRequest, updateAble } from '../GenericFunctions';

export async function getTableNames(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
	const returnData: INodePropertyOptions[] = [];
	const {
		metadata: { tables },
	} = await seaTableApiRequest.call(
		this,
		{},
		'GET',
		'/api-gateway/api/v2/dtables/{{dtable_uuid}}/metadata',
	);
	for (const table of tables) {
		returnData.push({
			name: table.name,
			value: table.name,
		});
	}
	return returnData;
}

export async function getTableNameAndId(
	this: ILoadOptionsFunctions,
): Promise<INodePropertyOptions[]> {
	const returnData: INodePropertyOptions[] = [];
	const {
		metadata: { tables },
	} = await seaTableApiRequest.call(
		this,
		{},
		'GET',
		'/api-gateway/api/v2/dtables/{{dtable_uuid}}/metadata',
	);
	for (const table of tables) {
		returnData.push({
			name: table.name,
			value: table.name + ':::' + table._id,
		});
	}
	return returnData;
}

export async function getSearchableColumns(
	this: ILoadOptionsFunctions,
): Promise<INodePropertyOptions[]> {
	const returnData: INodePropertyOptions[] = [];
	const tableName = this.getCurrentNodeParameter('tableName') as string;
	if (tableName) {
		const columns = await seaTableApiRequest.call(
			this,
			{},
			'GET',
			'/api-gateway/api/v2/dtables/{{dtable_uuid}}/columns',
			{},
			{ table_name: tableName },
		);
		for (const col of columns.columns) {
			if (
				col.type === 'text' ||
				col.type === 'long-text' ||
				col.type === 'number' ||
				col.type === 'single-select' ||
				col.type === 'email' ||
				col.type === 'url' ||
				col.type === 'rate' ||
				col.type === 'formula'
			) {
				returnData.push({
					name: col.name,
					value: col.name,
				});
			}
		}
	}
	return returnData;
}

export async function getLinkColumns(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
	const returnData: INodePropertyOptions[] = [];
	const table = this.getCurrentNodeParameter('tableName') as string;

	const tableName = table.split(':::')[0];
	const tableId = table.split(':::')[1];

	if (tableName) {
		const columns = await seaTableApiRequest.call(
			this,
			{},
			'GET',
			'/api-gateway/api/v2/dtables/{{dtable_uuid}}/columns',
			{},
			{ table_name: tableName },
		);
		for (const col of columns.columns) {
			if (col.type === 'link') {
				// make sure that the "other table id" is returned and not the same table id again.
				const otid =
					tableId !== col.data.other_table_id ? col.data.other_table_id : col.data.table_id;

				returnData.push({
					name: col.name,
					value: col.name + ':::' + col.data.link_id + ':::' + otid,
				});
			}
		}
	}
	return returnData;
}

export async function getLinkColumnsWithColumnKey(
	this: ILoadOptionsFunctions,
): Promise<INodePropertyOptions[]> {
	const returnData: INodePropertyOptions[] = [];
	const table = this.getCurrentNodeParameter('tableName') as string;

	const tableName = table.split(':::')[0];
	const tableId = table.split(':::')[1];

	if (tableName) {
		const columns = await seaTableApiRequest.call(
			this,
			{},
			'GET',
			'/api-gateway/api/v2/dtables/{{dtable_uuid}}/columns',
			{},
			{ table_name: tableName },
		);
		for (const col of columns.columns) {
			if (col.type === 'link') {
				// make sure that the "other table id" is returned and not the same table id again.
				const otid =
					tableId !== col.data.other_table_id ? col.data.other_table_id : col.data.table_id;

				returnData.push({
					name: col.name,
					value: col.name + ':::' + col.data.link_id + ':::' + otid + ':::' + col.key,
				});
			}
		}
	}
	return returnData;
}

export async function getAssetColumns(
	this: ILoadOptionsFunctions,
): Promise<INodePropertyOptions[]> {
	const returnData: INodePropertyOptions[] = [];
	const tableName = this.getCurrentNodeParameter('tableName') as string;
	if (tableName) {
		const columns = await seaTableApiRequest.call(
			this,
			{},
			'GET',
			'/api-gateway/api/v2/dtables/{{dtable_uuid}}/columns',
			{},
			{ table_name: tableName },
		);
		for (const col of columns.columns) {
			if (col.type === 'image' || col.type === 'file') {
				returnData.push({
					name: col.name,
					value: col.name + ':::' + col.type,
				});
			}
		}
	}
	return returnData;
}

export async function getSignatureColumns(
	this: ILoadOptionsFunctions,
): Promise<INodePropertyOptions[]> {
	const returnData: INodePropertyOptions[] = [];
	const tableName = this.getCurrentNodeParameter('tableName') as string;
	if (tableName) {
		// only execute if table is selected
		const columns = await seaTableApiRequest.call(
			this,
			{},
			'GET',
			'/api-gateway/api/v2/dtables/{{dtable_uuid}}/columns',
			{},
			{ table_name: tableName },
		);
		for (const col of columns.columns) {
			if (col.type === 'digital-sign') {
				returnData.push({
					name: col.name,
					value: col.name,
				});
			}
		}
	}
	return returnData;
}

export async function getTableUpdateAbleColumns(
	this: ILoadOptionsFunctions,
): Promise<INodePropertyOptions[]> {
	const tableName = this.getNodeParameter('tableName') as string;
	let columns = await getTableColumns.call(this, tableName);

	columns = updateAble(columns);

	return columns
		.filter((column) => column.editable)
		.map((column) => ({ name: column.name, value: column.name }));
}

export async function getRowIds(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
	const table = this.getCurrentNodeParameter('tableName') as string;
	const operation = this.getCurrentNodeParameter('operation') as string;
	let tableName = table;

	if (table.indexOf(':::') !== -1) {
		tableName = table.split(':::')[0];
	}

	let lockQuery = '';

	if (operation === 'lock') {
		lockQuery = 'WHERE _locked is null';
	}

	if (operation === 'unlock') {
		lockQuery = 'WHERE _locked = true';
	}

	const returnData: INodePropertyOptions[] = [];
	if (tableName) {
		const sqlResult = await seaTableApiRequest.call(
			this,
			{},
			'POST',
			'/api-gateway/api/v2/dtables/{{dtable_uuid}}/sql',
			{
				sql: `SELECT * FROM \`${tableName}\` ${lockQuery} LIMIT 1000`,
				convert_keys: false,
			},
		);
		const rows = sqlResult.results as IRow[];

		for (const row of rows) {
			returnData.push({
				name: `${row['0000'] as string} (${row._id})`,
				value: row._id,
			});
		}
	}
	return returnData;
}

export async function getTableViews(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
	const returnData: INodePropertyOptions[] = [];
	const tableName = this.getCurrentNodeParameter('tableName') as string;
	if (tableName) {
		const { views } = await seaTableApiRequest.call(
			this,
			{},
			'GET',
			'/api-gateway/api/v2/dtables/{{dtable_uuid}}/views',
			{},
			{ table_name: tableName },
		);
		returnData.push({
			name: '<Do not limit to a view>',
			value: '',
		});
		for (const view of views) {
			returnData.push({
				name: view.name,
				value: view.name,
			});
		}
	}
	return returnData;
}
