"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Venafi/Datacenter/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Venafi/Datacenter 的节点。导入/依赖:外部:lodash/get；内部:@n8n/errors；本地:无。导出:无。关键函数/方法:venafiApiRequest、venafiApiRequestAllItems。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Venafi/Datacenter/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Venafi/Datacenter/GenericFunctions.py

import get from 'lodash/get';
import { ApplicationError } from '@n8n/errors';
import type {
	IDataObject,
	IExecuteFunctions,
	IHttpRequestMethods,
	ILoadOptionsFunctions,
	IPollFunctions,
	IRequestOptions,
} from 'n8n-workflow';

export async function venafiApiRequest(
	this: IExecuteFunctions | ILoadOptionsFunctions | IPollFunctions,
	method: IHttpRequestMethods,
	resource: string,
	body: IDataObject = {},
	qs: IDataObject = {},
	uri?: string,
	headers: IDataObject = {},
): Promise<any> {
	const credentials = await this.getCredentials('venafiTlsProtectDatacenterApi');

	const options: IRequestOptions = {
		headers: {
			'Content-Type': 'application/json',
		},
		method,
		body,
		qs,
		rejectUnauthorized: !credentials.allowUnauthorizedCerts,
		uri: uri || `${credentials.domain}${resource}`,
		json: true,
	};

	try {
		if (Object.keys(headers).length !== 0) {
			options.headers = Object.assign({}, options.headers, headers);
		}
		if (Object.keys(body).length === 0) {
			delete options.body;
		}
		return await this.helpers.requestWithAuthentication.call(
			this,
			'venafiTlsProtectDatacenterApi',
			options,
		);
	} catch (error) {
		if (error.response?.body?.error) {
			let errors = error.response.body.error.errors;

			errors = errors.map((e: IDataObject) => e.message);
			// Try to return the error prettier
			throw new ApplicationError(
				`Venafi error response [${error.statusCode}]: ${errors.join('|')}`,
				{ level: 'warning' },
			);
		}
		throw error;
	}
}

export async function venafiApiRequestAllItems(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	propertyName: string,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject = {},
	query: IDataObject = {},
): Promise<any> {
	const returnData: IDataObject[] = [];

	let responseData;

	do {
		responseData = await venafiApiRequest.call(this, method, endpoint, body, query);
		endpoint = get(responseData, '_links[0].Next');
		returnData.push.apply(returnData, responseData[propertyName] as IDataObject[]);
	} while (responseData._links?.[0].Next);

	return returnData;
}
