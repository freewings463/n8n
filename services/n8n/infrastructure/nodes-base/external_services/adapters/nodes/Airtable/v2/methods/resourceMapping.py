"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtable/v2/methods/resourceMapping.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtable/v2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../transport。导出:无。关键函数/方法:mapForeignType、getColumns、tableData、constructOptions、getColumnsWithRecordId。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtable/v2/methods/resourceMapping.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtable/v2/methods/resourceMapping.py

import type {
	FieldType,
	IDataObject,
	ILoadOptionsFunctions,
	INodePropertyOptions,
	ResourceMapperField,
	ResourceMapperFields,
} from 'n8n-workflow';
import { NodeOperationError } from 'n8n-workflow';

import { apiRequest } from '../transport';

type AirtableSchema = {
	id: string;
	name: string;
	type: string;
	options?: IDataObject;
};

type TypesMap = Partial<Record<FieldType, string[]>>;

const airtableReadOnlyFields = [
	'autoNumber',
	'button',
	'count',
	'createdBy',
	'createdTime',
	'formula',
	'lastModifiedBy',
	'lastModifiedTime',
	'lookup',
	'rollup',
	'externalSyncSource',
	'multipleLookupValues',
];

const airtableTypesMap: TypesMap = {
	string: ['singleLineText', 'multilineText', 'richText', 'email', 'phoneNumber', 'url'],
	number: ['rating', 'percent', 'number', 'duration', 'currency'],
	boolean: ['checkbox'],
	dateTime: ['dateTime', 'date'],
	time: [],
	object: [],
	options: ['singleSelect'],
	array: ['multipleSelects', 'multipleRecordLinks', 'multipleAttachments'],
};

function mapForeignType(foreignType: string, typesMap: TypesMap): FieldType {
	let type: FieldType = 'string';

	for (const nativeType of Object.keys(typesMap)) {
		const mappedForeignTypes = typesMap[nativeType as FieldType];

		if (mappedForeignTypes?.includes(foreignType)) {
			type = nativeType as FieldType;
			break;
		}
	}

	return type;
}

export async function getColumns(this: ILoadOptionsFunctions): Promise<ResourceMapperFields> {
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

	const fields: ResourceMapperField[] = [];

	const constructOptions = (field: AirtableSchema) => {
		if (field?.options?.choices) {
			return (field.options.choices as IDataObject[]).map((choice) => ({
				name: choice.name,
				value: choice.name,
			})) as INodePropertyOptions[];
		}

		return undefined;
	};

	for (const field of tableData.fields as AirtableSchema[]) {
		const type = mapForeignType(field.type, airtableTypesMap);
		const isReadOnly = airtableReadOnlyFields.includes(field.type);
		const options = constructOptions(field);
		fields.push({
			id: field.name,
			displayName: field.name,
			required: false,
			defaultMatch: false,
			canBeUsedToMatch: true,
			display: true,
			type,
			options,
			readOnly: isReadOnly,
			removed: isReadOnly,
		});
	}

	return { fields };
}

export async function getColumnsWithRecordId(
	this: ILoadOptionsFunctions,
): Promise<ResourceMapperFields> {
	const returnData = await getColumns.call(this);
	return {
		fields: [
			{
				id: 'id',
				displayName: 'id',
				required: false,
				defaultMatch: true,
				display: true,
				type: 'string',
				readOnly: true,
			},
			...returnData.fields,
		],
	};
}
