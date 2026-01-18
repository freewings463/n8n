"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Odoo/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Odoo 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:mapOperationToJSONRPC、mapOdooResources、mapFilterOperationToJSONRPC、IOdooFilterOperations、IOdooNameValueFields、IOdooResponseFields、odooGetDBName、processNameValueFields。关键函数/方法:odooGetDBName、processFilters、processNameValueFields、odooJSONRPCRequest、odooGetModelFields、odooCreate、odooGet 等5项。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Odoo/GenericFunctions.ts -> services/n8n/tests/nodes-base/unit/nodes/Odoo/GenericFunctions.py

import type {
	IDataObject,
	IExecuteFunctions,
	IHookFunctions,
	ILoadOptionsFunctions,
	JsonObject,
	IRequestOptions,
} from 'n8n-workflow';
import { NodeApiError, randomInt } from 'n8n-workflow';

const serviceJSONRPC = 'object';
const methodJSONRPC = 'execute';

export const mapOperationToJSONRPC = {
	create: 'create',
	get: 'read',
	getAll: 'search_read',
	update: 'write',
	delete: 'unlink',
};

export const mapOdooResources: { [key: string]: string } = {
	contact: 'res.partner',
	opportunity: 'crm.lead',
	note: 'note.note',
};

export const mapFilterOperationToJSONRPC = {
	equal: '=',
	notEqual: '!=',
	greaterThen: '>',
	lesserThen: '<',
	greaterOrEqual: '>=',
	lesserOrEqual: '<=',
	like: 'like',
	in: 'in',
	notIn: 'not in',
	childOf: 'child_of',
};

type FilterOperation =
	| 'equal'
	| 'notEqual'
	| 'greaterThen'
	| 'lesserThen'
	| 'greaterOrEqual'
	| 'lesserOrEqual'
	| 'like'
	| 'in'
	| 'notIn'
	| 'childOf';

export interface IOdooFilterOperations {
	filter: Array<{
		fieldName: string;
		operator: string;
		value: string;
	}>;
}

export interface IOdooNameValueFields {
	fields: Array<{
		fieldName: string;
		fieldValue: string;
	}>;
}

export interface IOdooResponseFields {
	fields: Array<{
		field: string;
		fromList?: boolean;
	}>;
}

type OdooCRUD = 'create' | 'update' | 'delete' | 'get' | 'getAll';

export function odooGetDBName(databaseName: string | undefined, url: string) {
	if (databaseName) return databaseName;
	const odooURL = new URL(url);
	const hostname = odooURL.hostname;
	if (!hostname) return '';
	return odooURL.hostname.split('.')[0];
}

function processFilters(value: IOdooFilterOperations) {
	return value.filter?.map((item) => {
		const operator = item.operator as FilterOperation;
		item.operator = mapFilterOperationToJSONRPC[operator];
		return Object.values(item);
	});
}

export function processNameValueFields(value: IDataObject) {
	const data = value as unknown as IOdooNameValueFields;
	return data?.fields?.reduce((acc, record) => {
		return Object.assign(acc, { [record.fieldName]: record.fieldValue });
	}, {});
}

// function processResponseFields(value: IDataObject) {
// 	const data = value as unknown as IOdooResponseFields;
// 	return data?.fields?.map((entry) => entry.field);
// }

export async function odooJSONRPCRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	body: IDataObject,
	url: string,
): Promise<IDataObject | IDataObject[]> {
	try {
		const options: IRequestOptions = {
			headers: {
				'User-Agent': 'n8n',
				Connection: 'keep-alive',
				Accept: '*/*',
				'Content-Type': 'application/json',
			},
			method: 'POST',
			body,
			uri: `${url}/jsonrpc`,
			json: true,
		};

		const response = await this.helpers.request(options);
		if (response.error) {
			throw new NodeApiError(this.getNode(), response.error.data as JsonObject, {
				message: response.error.data.message,
			});
		}
		return response.result;
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function odooGetModelFields(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	db: string,
	userID: number,
	password: string,
	resource: string,
	url: string,
) {
	try {
		const body = {
			jsonrpc: '2.0',
			method: 'call',
			params: {
				service: serviceJSONRPC,
				method: methodJSONRPC,
				args: [
					db,
					userID,
					password,
					mapOdooResources[resource] || resource,
					'fields_get',
					[],
					['string', 'type', 'help', 'required', 'name'],
				],
			},
			id: randomInt(100),
		};

		const result = await odooJSONRPCRequest.call(this, body, url);
		return result;
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function odooCreate(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	db: string,
	userID: number,
	password: string,
	resource: string,
	operation: OdooCRUD,
	url: string,
	newItem: IDataObject,
) {
	try {
		const body = {
			jsonrpc: '2.0',
			method: 'call',
			params: {
				service: serviceJSONRPC,
				method: methodJSONRPC,
				args: [
					db,
					userID,
					password,
					mapOdooResources[resource] || resource,
					mapOperationToJSONRPC[operation],
					newItem || {},
				],
			},
			id: randomInt(100),
		};

		const result = await odooJSONRPCRequest.call(this, body, url);
		return { id: result };
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function odooGet(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	db: string,
	userID: number,
	password: string,
	resource: string,
	operation: OdooCRUD,
	url: string,
	itemsID: string,
	fieldsToReturn?: IDataObject[],
) {
	try {
		if (!/^\d+$/.test(itemsID) || !parseInt(itemsID, 10)) {
			throw new NodeApiError(this.getNode(), {
				status: 'Error',
				message: `Please specify a valid ID: ${itemsID}`,
			});
		}
		const body = {
			jsonrpc: '2.0',
			method: 'call',
			params: {
				service: serviceJSONRPC,
				method: methodJSONRPC,
				args: [
					db,
					userID,
					password,
					mapOdooResources[resource] || resource,
					mapOperationToJSONRPC[operation],
					itemsID ? [+itemsID] : [],
					fieldsToReturn || [],
				],
			},
			id: randomInt(100),
		};

		const result = await odooJSONRPCRequest.call(this, body, url);
		return result;
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function odooGetAll(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	db: string,
	userID: number,
	password: string,
	resource: string,
	operation: OdooCRUD,
	url: string,
	filters?: IOdooFilterOperations,
	fieldsToReturn?: IDataObject[],
	limit = 0,
) {
	try {
		const body = {
			jsonrpc: '2.0',
			method: 'call',
			params: {
				service: serviceJSONRPC,
				method: methodJSONRPC,
				args: [
					db,
					userID,
					password,
					mapOdooResources[resource] || resource,
					mapOperationToJSONRPC[operation],
					(filters && processFilters(filters)) || [],
					fieldsToReturn || [],
					0, // offset
					limit,
				],
			},
			id: randomInt(100),
		};

		const result = await odooJSONRPCRequest.call(this, body, url);
		return result;
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function odooUpdate(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	db: string,
	userID: number,
	password: string,
	resource: string,
	operation: OdooCRUD,
	url: string,
	itemsID: string,
	fieldsToUpdate: IDataObject,
) {
	try {
		if (!Object.keys(fieldsToUpdate).length) {
			throw new NodeApiError(this.getNode(), {
				status: 'Error',
				message: 'Please specify at least one field to update',
			});
		}
		if (!/^\d+$/.test(itemsID) || !parseInt(itemsID, 10)) {
			throw new NodeApiError(this.getNode(), {
				status: 'Error',
				message: `Please specify a valid ID: ${itemsID}`,
			});
		}
		const body = {
			jsonrpc: '2.0',
			method: 'call',
			params: {
				service: serviceJSONRPC,
				method: methodJSONRPC,
				args: [
					db,
					userID,
					password,
					mapOdooResources[resource] || resource,
					mapOperationToJSONRPC[operation],
					itemsID ? [+itemsID] : [],
					fieldsToUpdate,
				],
			},
			id: randomInt(100),
		};

		await odooJSONRPCRequest.call(this, body, url);
		return { id: itemsID };
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function odooDelete(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	db: string,
	userID: number,
	password: string,
	resource: string,
	operation: OdooCRUD,
	url: string,
	itemsID: string,
) {
	if (!/^\d+$/.test(itemsID) || !parseInt(itemsID, 10)) {
		throw new NodeApiError(this.getNode(), {
			status: 'Error',
			message: `Please specify a valid ID: ${itemsID}`,
		});
	}
	try {
		const body = {
			jsonrpc: '2.0',
			method: 'call',
			params: {
				service: serviceJSONRPC,
				method: methodJSONRPC,
				args: [
					db,
					userID,
					password,
					mapOdooResources[resource] || resource,
					mapOperationToJSONRPC[operation],
					itemsID ? [+itemsID] : [],
				],
			},
			id: randomInt(100),
		};

		await odooJSONRPCRequest.call(this, body, url);
		return { success: true };
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function odooGetUserID(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	db: string,
	username: string,
	password: string,
	url: string,
): Promise<number> {
	try {
		const body = {
			jsonrpc: '2.0',
			method: 'call',
			params: {
				service: 'common',
				method: 'login',
				args: [db, username, password],
			},
			id: randomInt(100),
		};
		const loginResult = await odooJSONRPCRequest.call(this, body, url);
		return loginResult as unknown as number;
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function odooGetServerVersion(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	url: string,
) {
	try {
		const body = {
			jsonrpc: '2.0',
			method: 'call',
			params: {
				service: 'common',
				method: 'version',
				args: [],
			},
			id: randomInt(100),
		};
		const result = await odooJSONRPCRequest.call(this, body, url);
		return result;
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}
