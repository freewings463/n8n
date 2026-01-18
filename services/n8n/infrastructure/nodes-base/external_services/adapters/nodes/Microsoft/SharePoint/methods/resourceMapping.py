"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/SharePoint/methods/resourceMapping.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/SharePoint 的节点。导入/依赖:外部:无；内部:无；本地:../helpers/interfaces、../transport。导出:无。关键函数/方法:mapType、getMappingColumns。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/SharePoint/methods/resourceMapping.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/SharePoint/methods/resourceMapping.py

import type {
	FieldType,
	ILoadOptionsFunctions,
	ResourceMapperField,
	ResourceMapperFields,
} from 'n8n-workflow';

import type { IListColumnType } from '../helpers/interfaces';
import { microsoftSharePointApiRequest } from '../transport';

const unsupportedFields = ['geoLocation', 'location', 'term', 'url'];
const fieldTypeMapping: Partial<Record<FieldType, string[]>> = {
	string: ['text', 'user', 'lookup'],
	// unknownFutureValue: rating
	number: ['number', 'currency', 'unknownFutureValue'],
	boolean: ['boolean'],
	dateTime: ['dateTime'],
	object: ['thumbnail'],
	options: ['choice'],
};

function mapType(column: IListColumnType): FieldType | undefined {
	if (unsupportedFields.includes(column.type)) {
		return undefined;
	}
	let mappedType: FieldType = 'string';
	for (const t of Object.keys(fieldTypeMapping)) {
		const postgresTypes = fieldTypeMapping[t as FieldType];
		if (postgresTypes?.includes(column.type)) {
			mappedType = t as FieldType;
		}
	}
	return mappedType;
}

export async function getMappingColumns(
	this: ILoadOptionsFunctions,
): Promise<ResourceMapperFields> {
	const site = this.getNodeParameter('site', undefined, { extractValue: true }) as string;
	const list = this.getNodeParameter('list', undefined, { extractValue: true }) as string;
	const operation = this.getNodeParameter('operation') as string;

	const response = await microsoftSharePointApiRequest.call(
		this,
		'GET',
		`/sites/${site}/lists/${list}/contentTypes`,
		{},
		{ expand: 'columns' },
	);

	const columns: IListColumnType[] = response.value[0].columns;

	const fields: ResourceMapperField[] = [];

	for (const column of columns.filter((x) => !x.hidden && !x.readOnly)) {
		const fieldType = mapType(column);
		const field = {
			id: column.name,
			canBeUsedToMatch: column.enforceUniqueValues && column.required,
			defaultMatch: false,
			display: true,
			displayName: column.displayName,
			readOnly: column.readOnly || !fieldType,
			required: column.required,
			type: fieldType,
		} as ResourceMapperField;
		if (field.type === 'options') {
			field.options = [];
			if (Array.isArray(column.choice?.choices)) {
				for (const choice of column.choice.choices) {
					field.options.push({
						name: choice,
						value: choice,
					});
				}
			}
		}
		fields.push(field);
	}

	if (operation === 'update') {
		fields.push({
			id: 'id',
			canBeUsedToMatch: true,
			defaultMatch: false,
			display: true,
			displayName: 'ID',
			readOnly: true,
			required: true,
			type: 'string',
		});
	}

	return { fields };
}
