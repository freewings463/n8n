"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/PhilipsHue/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/PhilipsHue 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:philipsHueApiRequest、getUser。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/PhilipsHue/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/PhilipsHue/GenericFunctions.py

import type {
	JsonObject,
	IDataObject,
	IExecuteFunctions,
	ILoadOptionsFunctions,
	IHttpRequestMethods,
	IRequestOptions,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

export async function philipsHueApiRequest(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	resource: string,

	body: any = {},
	qs: IDataObject = {},
	uri?: string,
	headers: IDataObject = {},
): Promise<any> {
	const options: IRequestOptions = {
		headers: {
			'Content-Type': 'application/json',
		},
		method,
		body,
		qs,
		uri: uri || `https://api.meethue.com/route${resource}`,
		json: true,
	};
	try {
		if (Object.keys(headers).length !== 0) {
			options.headers = Object.assign({}, options.headers, headers);
		}

		if (Object.keys(body as IDataObject).length === 0) {
			delete options.body;
		}

		if (Object.keys(qs).length === 0) {
			delete options.qs;
		}

		const response = await this.helpers.requestOAuth2.call(this, 'philipsHueOAuth2Api', options, {
			tokenType: 'Bearer',
		});
		return response;
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function getUser(this: IExecuteFunctions | ILoadOptionsFunctions): Promise<any> {
	const { whitelist } = await philipsHueApiRequest.call(this, 'GET', '/api/0/config', {}, {});
	//check if there is a n8n user
	for (const user of Object.keys(whitelist as IDataObject)) {
		if (whitelist[user].name === 'n8n') {
			return user;
		}
	}
	// n8n user was not fount then create the user
	await philipsHueApiRequest.call(this, 'PUT', '/api/0/config', { linkbutton: true });
	const { success } = await philipsHueApiRequest.call(this, 'POST', '/api', { devicetype: 'n8n' });
	return success.username;
}
