"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/LinkedIn/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/LinkedIn 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:validateJSON。关键函数/方法:resolveHeaderData、linkedInApiRequest、validateJSON。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/LinkedIn/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/LinkedIn/GenericFunctions.py

import type {
	IDataObject,
	IExecuteFunctions,
	IHookFunctions,
	ILoadOptionsFunctions,
	JsonObject,
	IRequestOptions,
	IHttpRequestMethods,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';
function resolveHeaderData(fullResponse: any) {
	if (fullResponse.statusCode === 201) {
		return { urn: fullResponse.headers['x-restli-id'] };
	} else {
		return fullResponse.body;
	}
}

export async function linkedInApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,

	body: any = {},
	binary?: boolean,
	_headers?: object,
): Promise<any> {
	const authenticationMethod = this.getNodeParameter('authentication', 0);
	const credentialType =
		authenticationMethod === 'standard'
			? 'linkedInOAuth2Api'
			: 'linkedInCommunityManagementOAuth2Api';

	const baseUrl = 'https://api.linkedin.com';

	let options: IRequestOptions = {
		headers: {
			Accept: 'application/json',
			'X-Restli-Protocol-Version': '2.0.0',
			'LinkedIn-Version': '202504',
		},
		method,
		body,
		url: binary ? endpoint : `${baseUrl}${endpoint.includes('v2') ? '' : '/rest'}${endpoint}`,
		json: true,
	};

	options = Object.assign({}, options, {
		resolveWithFullResponse: true,
	});
	// If uploading binary data
	if (binary) {
		delete options.json;
		options.encoding = null;
		if (Object.keys(_headers as object).length > 0) {
			Object.assign(options.headers as object, _headers);
		}
	}

	if (Object.keys(body as IDataObject).length === 0) {
		delete options.body;
	}

	try {
		return resolveHeaderData(
			await this.helpers.requestOAuth2.call(this, credentialType, options, {
				tokenType: 'Bearer',
			}),
		);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export function validateJSON(json: string | undefined): any {
	let result;
	try {
		result = JSON.parse(json!);
	} catch (exception) {
		result = '';
	}
	return result;
}
