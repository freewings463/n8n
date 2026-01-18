"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtable/v2/methods/loadOptions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtable/v2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../transport。导出:无。关键函数/方法:getColumns、tableData、getColumnsWithRecordId、getColumnsWithoutColumnToMatchOn、getAttachmentColumns。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtable/v2/methods/loadOptions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtable/v2/methods/loadOptions.py

import type { IDataObject, ILoadOptionsFunctions, INodePropertyOptions } from 'n8n-workflow';
import { NodeOperationError } from 'n8n-workflow';

import { apiRequest } from '../transport';

export async function getColumns(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
	const base = this.getNodeParameter('base', undefined, {
		extractValue: true,
	}) as string;

	const tableId = encodeURI(
		this.getNodeParameter('table', undefined, {
			extractValue: true,
		}) as string,
	);

	const response = await apiRequest.call(this, 'GET', `meta/bases/${base}/tables`);

	const tableData = ((response.tables as IDataObject[]) || []).find((table: IDataObject) => {
		return table.id === tableId;
	});

	if (!tableData) {
		throw new NodeOperationError(this.getNode(), 'Table information could not be found!', {
			level: 'warning',
		});
	}

	const result: INodePropertyOptions[] = [];

	for (const field of tableData.fields as IDataObject[]) {
		result.push({
			name: field.name as string,
			value: field.name as string,
			description: `Type: ${field.type}`,
		});
	}

	return result;
}

export async function getColumnsWithRecordId(
	this: ILoadOptionsFunctions,
): Promise<INodePropertyOptions[]> {
	const returnData = await getColumns.call(this);
	return [
		{
			// eslint-disable-next-line n8n-nodes-base/node-param-display-name-miscased-id, n8n-nodes-base/node-param-display-name-miscased
			name: 'id',
			value: 'id' as string,
			description: 'Type: primaryFieldId',
		},
		...returnData,
	];
}

export async function getColumnsWithoutColumnToMatchOn(
	this: ILoadOptionsFunctions,
): Promise<INodePropertyOptions[]> {
	const columnToMatchOn = this.getNodeParameter('columnToMatchOn') as string;
	const returnData = await getColumns.call(this);
	return returnData.filter((column) => column.value !== columnToMatchOn);
}

export async function getAttachmentColumns(
	this: ILoadOptionsFunctions,
): Promise<INodePropertyOptions[]> {
	const base = this.getNodeParameter('base', undefined, {
		extractValue: true,
	}) as string;

	const tableId = encodeURI(
		this.getNodeParameter('table', undefined, {
			extractValue: true,
		}) as string,
	);

	const response = await apiRequest.call(this, 'GET', `meta/bases/${base}/tables`);

	const tableData = ((response.tables as IDataObject[]) || []).find((table: IDataObject) => {
		return table.id === tableId;
	});

	if (!tableData) {
		throw new NodeOperationError(this.getNode(), 'Table information could not be found!', {
			level: 'warning',
		});
	}

	const result: INodePropertyOptions[] = [];

	for (const field of tableData.fields as IDataObject[]) {
		if (!(field.type as string)?.toLowerCase()?.includes('attachment')) {
			continue;
		}
		result.push({
			name: field.name as string,
			value: field.name as string,
			description: `Type: ${field.type}`,
		});
	}

	return result;
}
