"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Github/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Github 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:isBase64、validateJSON。关键函数/方法:githubApiRequest、getFileSha、githubApiRequestAllItems、isBase64、validateJSON。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Github/GenericFunctions.ts -> services/n8n/tests/nodes-base/unit/nodes/Github/GenericFunctions.py

import type {
	IExecuteFunctions,
	IHookFunctions,
	IDataObject,
	ILoadOptionsFunctions,
	JsonObject,
	IHttpRequestMethods,
	IRequestOptions,
} from 'n8n-workflow';
import { NodeApiError, NodeOperationError } from 'n8n-workflow';

/**
 * Make an API request to Github
 *
 */
export async function githubApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: object,
	query?: IDataObject,
	option: IDataObject = {},
): Promise<any> {
	const options: IRequestOptions = {
		method,
		headers: {
			'User-Agent': 'n8n',
		},
		body,
		qs: query,
		uri: '',
		json: true,
	};

	if (Object.keys(option).length !== 0) {
		Object.assign(options, option);
	}

	try {
		const authenticationMethod = this.getNodeParameter(
			'authentication',
			0,
			'accessToken',
		) as string;
		let credentialType = '';

		if (authenticationMethod === 'accessToken') {
			const credentials = await this.getCredentials('githubApi');
			credentialType = 'githubApi';

			const baseUrl = credentials.server || 'https://api.github.com';
			options.uri = `${baseUrl}${endpoint}`;
		} else {
			const credentials = await this.getCredentials('githubOAuth2Api');
			credentialType = 'githubOAuth2Api';

			const baseUrl = credentials.server || 'https://api.github.com';
			options.uri = `${baseUrl}${endpoint}`;
		}

		return await this.helpers.requestWithAuthentication.call(this, credentialType, options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

/**
 * Returns the SHA of the given file
 *
 * @param {(IHookFunctions | IExecuteFunctions)} this
 */
export async function getFileSha(
	this: IHookFunctions | IExecuteFunctions,
	owner: string,
	repository: string,
	filePath: string,
	branch?: string,
): Promise<any> {
	const query: IDataObject = {};
	if (branch !== undefined) {
		query.ref = branch;
	}

	const getEndpoint = `/repos/${owner}/${repository}/contents/${encodeURI(filePath)}`;
	const responseData = await githubApiRequest.call(this, 'GET', getEndpoint, {}, query);

	if (responseData.sha === undefined) {
		throw new NodeOperationError(this.getNode(), 'Could not get the SHA of the file.');
	}
	return responseData.sha;
}

export async function githubApiRequestAllItems(
	this: IHookFunctions | IExecuteFunctions,
	method: IHttpRequestMethods,
	endpoint: string,

	body: any = {},
	query: IDataObject = {},
): Promise<any> {
	const returnData: IDataObject[] = [];

	let responseData;

	query.per_page = 100;
	query.page = 1;

	do {
		responseData = await githubApiRequest.call(this, method, endpoint, body as IDataObject, query, {
			resolveWithFullResponse: true,
		});
		query.page++;
		returnData.push.apply(returnData, responseData.body as IDataObject[]);
	} while (responseData.headers.link?.includes('next'));
	return returnData;
}

export function isBase64(content: string) {
	const base64regex = /^([0-9a-zA-Z+/]{4})*(([0-9a-zA-Z+/]{2}==)|([0-9a-zA-Z+/]{3}=))?$/;
	return base64regex.test(content);
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
