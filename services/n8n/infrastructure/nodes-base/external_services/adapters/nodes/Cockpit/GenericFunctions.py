"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Cockpit/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Cockpit 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:createDataFromParameters。关键函数/方法:cockpitApiRequest、createDataFromParameters。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Cockpit/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Cockpit/GenericFunctions.py

import type {
	IDataObject,
	IExecuteFunctions,
	IHttpRequestMethods,
	ILoadOptionsFunctions,
	IRequestOptions,
	JsonObject,
} from 'n8n-workflow';
import { jsonParse, NodeApiError } from 'n8n-workflow';

export async function cockpitApiRequest(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	resource: string,

	body: any = {},
	uri?: string,
	option: IDataObject = {},
): Promise<any> {
	const credentials = await this.getCredentials('cockpitApi');
	let options: IRequestOptions = {
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
		},
		method,
		qs: {
			token: credentials.accessToken,
		},
		body,
		uri: uri || `${credentials.url}/api${resource}`,
		json: true,
	};

	options = Object.assign({}, options, option);

	if (Object.keys(options.body as IDataObject).length === 0) {
		delete options.body;
	}

	try {
		return await this.helpers.request(options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export function createDataFromParameters(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	itemIndex: number,
): IDataObject {
	const dataFieldsAreJson = this.getNodeParameter('jsonDataFields', itemIndex) as boolean;

	if (dataFieldsAreJson) {
		// Parameters are defined as JSON
		return jsonParse(this.getNodeParameter('dataFieldsJson', itemIndex, '{}') as string);
	}

	// Parameters are defined in UI
	const uiDataFields = this.getNodeParameter('dataFieldsUi', itemIndex, {}) as IDataObject;
	const unpacked: IDataObject = {};

	if (uiDataFields.field === undefined) {
		return unpacked;
	}

	for (const field of uiDataFields.field as IDataObject[]) {
		unpacked[field.name as string] = field.value;
	}

	return unpacked;
}
