"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Zendesk/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Zendesk 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:validateJSON。关键函数/方法:getUri、zendeskApiRequest、zendeskApiRequestAllItems、validateJSON。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Zendesk/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Zendesk/GenericFunctions.py

import type {
	IDataObject,
	IExecuteFunctions,
	IHookFunctions,
	ILoadOptionsFunctions,
	IHttpRequestMethods,
	IRequestOptions,
} from 'n8n-workflow';

function getUri(resource: string, subdomain: string) {
	if (resource.includes('webhooks')) {
		return `https://${subdomain}.zendesk.com/api/v2${resource}`;
	} else {
		return `https://${subdomain}.zendesk.com/api/v2${resource}.json`;
	}
}

export async function zendeskApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	resource: string,

	body: any = {},
	qs: IDataObject = {},
	uri?: string,
	option: IDataObject = {},
) {
	const authenticationMethod = this.getNodeParameter('authentication', 0);

	let credentials;

	if (authenticationMethod === 'apiToken') {
		credentials = await this.getCredentials<{ subdomain: string }>('zendeskApi');
	} else {
		credentials = await this.getCredentials<{ subdomain: string }>('zendeskOAuth2Api');
	}

	let options: IRequestOptions = {
		method,
		qs,
		body,
		uri: uri || getUri(resource, credentials.subdomain),
		json: true,
		qsStringifyOptions: {
			arrayFormat: 'brackets',
		},
	};

	options = Object.assign({}, options, option);
	if (Object.keys(options.body as IDataObject).length === 0) {
		delete options.body;
	}

	const credentialType = authenticationMethod === 'apiToken' ? 'zendeskApi' : 'zendeskOAuth2Api';

	return await this.helpers.requestWithAuthentication.call(this, credentialType, options);
}

/**
 * Make an API request to paginated flow endpoint
 * and return all results
 */
export async function zendeskApiRequestAllItems(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	propertyName: string,
	method: IHttpRequestMethods,
	resource: string,

	body: any = {},
	query: IDataObject = {},
): Promise<any> {
	const returnData: IDataObject[] = [];

	let responseData;

	let uri: string | undefined;

	do {
		responseData = await zendeskApiRequest.call(this, method, resource, body, query, uri);
		uri = responseData.next_page;
		returnData.push.apply(returnData, responseData[propertyName] as IDataObject[]);
		const limit = query.limit as number | undefined;
		if (limit && limit <= returnData.length) {
			return returnData;
		}
	} while (responseData.next_page !== undefined && responseData.next_page !== null);

	return returnData;
}

export function validateJSON(json: string | undefined): any {
	let result;
	try {
		result = JSON.parse(json!);
	} catch (exception) {
		result = undefined;
	}
	return result;
}
