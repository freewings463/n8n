"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/BambooHr/v1/methods/loadOptions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/BambooHr/v1 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../transport。导出:无。关键函数/方法:getTimeOffTypeID、sort、getCompanyFileCategories、getEmployeeDocumentCategories、getEmployeeLocations、fields、getDepartments、getDivisions、getEmployeeFields。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/BambooHr/v1/methods/loadOptions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/BambooHr/v1/methods/loadOptions.py

import type { IDataObject, ILoadOptionsFunctions, INodePropertyOptions } from 'n8n-workflow';

import { apiRequest } from '../transport';

// Get all the available channels
export async function getTimeOffTypeID(
	this: ILoadOptionsFunctions,
): Promise<INodePropertyOptions[]> {
	const returnData: INodePropertyOptions[] = [];
	const body: IDataObject = {};
	const requestMethod = 'GET';
	const endPoint = 'meta/time_off/types';

	const response = await apiRequest.call(this, requestMethod, endPoint, body);
	const timeOffTypeIds = response.body.timeOffTypes;

	for (const item of timeOffTypeIds) {
		returnData.push({
			name: item.name,
			value: item.id,
		});
	}
	return returnData;
}

//@ts-ignore
const sort = (a, b) => {
	if (a.name.toLocaleLowerCase() < b.name.toLocaleLowerCase()) {
		return -1;
	}
	if (a.name.toLocaleLowerCase() > b.name.toLocaleLowerCase()) {
		return 1;
	}
	return 0;
};

export async function getCompanyFileCategories(
	this: ILoadOptionsFunctions,
): Promise<INodePropertyOptions[]> {
	const returnData: INodePropertyOptions[] = [];
	const body: IDataObject = {};
	const requestMethod = 'GET';
	const endPoint = 'files/view/';

	const response = await apiRequest.call(this, requestMethod, endPoint, body);
	const categories = response.categories;

	for (const category of categories) {
		returnData.push({
			name: category.name,
			value: category.id,
		});
	}

	returnData.sort(sort);

	return returnData;
}

export async function getEmployeeDocumentCategories(
	this: ILoadOptionsFunctions,
): Promise<INodePropertyOptions[]> {
	const returnData: INodePropertyOptions[] = [];
	const body: IDataObject = {};
	const requestMethod = 'GET';
	const id = this.getCurrentNodeParameter('employeeId') as string;

	const endPoint = `employees/${id}/files/view/`;

	const response = await apiRequest.call(this, requestMethod, endPoint, body);
	const categories = response.categories;

	for (const category of categories) {
		returnData.push({
			name: category.name,
			value: category.id,
		});
	}

	returnData.sort(sort);

	return returnData;
}

export async function getEmployeeLocations(
	this: ILoadOptionsFunctions,
): Promise<INodePropertyOptions[]> {
	const returnData: INodePropertyOptions[] = [];
	const body: IDataObject = {};
	const requestMethod = 'GET';
	const endPoint = 'meta/lists/';

	//do not request all data?
	const fields = (await apiRequest.call(this, requestMethod, endPoint, body, {})) as [
		{ fieldId: number; options: [{ id: number; name: string }] },
	];

	const options = fields.filter((field) => field.fieldId === 18)[0].options;

	for (const option of options) {
		returnData.push({
			name: option.name,
			value: option.id,
		});
	}

	returnData.sort(sort);

	return returnData;
}

export async function getDepartments(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
	const returnData: INodePropertyOptions[] = [];
	const body: IDataObject = {};
	const requestMethod = 'GET';
	const endPoint = 'meta/lists/';

	//do not request all data?
	const fields = (await apiRequest.call(this, requestMethod, endPoint, body, {})) as [
		{ fieldId: number; options: [{ id: number; name: string }] },
	];

	const options = fields.filter((field) => field.fieldId === 4)[0].options;

	for (const option of options) {
		returnData.push({
			name: option.name,
			value: option.id,
		});
	}

	returnData.sort(sort);

	return returnData;
}

export async function getDivisions(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
	const returnData: INodePropertyOptions[] = [];
	const body: IDataObject = {};
	const requestMethod = 'GET';
	const endPoint = 'meta/lists/';

	//do not request all data?
	const fields = (await apiRequest.call(this, requestMethod, endPoint, body, {})) as [
		{ fieldId: number; options: [{ id: number; name: string }] },
	];

	const options = fields.filter((field) => field.fieldId === 1355)[0].options;

	for (const option of options) {
		returnData.push({
			name: option.name,
			value: option.id,
		});
	}

	returnData.sort(sort);

	return returnData;
}

export async function getEmployeeFields(
	this: ILoadOptionsFunctions,
): Promise<INodePropertyOptions[]> {
	const returnData: INodePropertyOptions[] = [];
	const body: IDataObject = {};
	const requestMethod = 'GET';
	const endPoint = 'employees/directory';

	const { fields } = await apiRequest.call(this, requestMethod, endPoint, body);

	for (const field of fields) {
		returnData.push({
			name: field.name || field.id,
			value: field.id,
		});
	}

	returnData.sort(sort);

	returnData.unshift({
		name: '[All]',
		value: 'all',
	});

	return returnData;
}
