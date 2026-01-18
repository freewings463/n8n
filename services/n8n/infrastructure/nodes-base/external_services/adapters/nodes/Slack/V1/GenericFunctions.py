"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Slack/V1/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Slack/V1 的节点。导入/依赖:外部:lodash/get；内部:n8n-workflow；本地:无。导出:validateJSON。关键函数/方法:slackApiRequest、slackApiRequestAllItems、validateJSON。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Slack/V1/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Slack/V1/GenericFunctions.py

import get from 'lodash/get';
import type {
	IExecuteFunctions,
	ILoadOptionsFunctions,
	IDataObject,
	IOAuth2Options,
	JsonObject,
	IHttpRequestMethods,
	IRequestOptions,
} from 'n8n-workflow';
import { NodeApiError, NodeOperationError } from 'n8n-workflow';

export async function slackApiRequest(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	resource: string,
	body: object = {},
	query: IDataObject = {},
	headers: IDataObject | undefined = undefined,
	option: IDataObject = {},
): Promise<any> {
	const authenticationMethod = this.getNodeParameter('authentication', 0, 'accessToken') as string;
	let options: IRequestOptions = {
		method,
		headers: headers || {
			'Content-Type': 'application/json; charset=utf-8',
		},
		body,
		qs: query,
		uri: `https://slack.com/api${resource}`,
		json: true,
	};
	options = Object.assign({}, options, option);
	if (Object.keys(body).length === 0) {
		delete options.body;
	}
	if (Object.keys(query).length === 0) {
		delete options.qs;
	}

	const oAuth2Options: IOAuth2Options = {
		tokenType: 'Bearer',
		property: 'authed_user.access_token',
	};

	try {
		const credentialType = authenticationMethod === 'accessToken' ? 'slackApi' : 'slackOAuth2Api';
		const response = await this.helpers.requestWithAuthentication.call(
			this,
			credentialType,
			options,
			{
				oauth2: oAuth2Options,
			},
		);

		if (response.ok === false) {
			if (response.error === 'paid_teams_only') {
				throw new NodeOperationError(
					this.getNode(),
					`Your current Slack plan does not include the resource '${this.getNodeParameter(
						'resource',
						0,
					)}'`,
					{
						description:
							'Hint: Upgrate to the Slack plan that includes the funcionality you want to use.',
					},
				);
			}

			throw new NodeOperationError(
				this.getNode(),
				'Slack error response: ' + JSON.stringify(response),
			);
		}

		return response;
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function slackApiRequestAllItems(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	propertyName: string,
	method: IHttpRequestMethods,
	endpoint: string,

	body: any = {},
	query: IDataObject = {},
): Promise<any> {
	const returnData: IDataObject[] = [];
	let responseData;
	query.page = 1;
	//if the endpoint uses legacy pagination use count
	//https://api.slack.com/docs/pagination#classic
	if (endpoint.includes('files.list')) {
		query.count = 100;
	} else {
		query.limit = 100;
	}
	do {
		responseData = await slackApiRequest.call(this, method, endpoint, body as IDataObject, query);
		query.cursor = get(responseData, 'response_metadata.next_cursor');
		query.page++;
		returnData.push.apply(returnData, responseData[propertyName] as IDataObject[]);
	} while (
		(responseData.response_metadata?.next_cursor !== undefined &&
			responseData.response_metadata.next_cursor !== '' &&
			responseData.response_metadata.next_cursor !== null) ||
		(responseData.paging?.pages !== undefined &&
			responseData.paging.page !== undefined &&
			responseData.paging.page < responseData.paging.pages)
	);

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
