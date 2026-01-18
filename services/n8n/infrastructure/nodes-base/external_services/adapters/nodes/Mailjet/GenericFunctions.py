"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Mailjet/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Mailjet 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:validateJSON、IMessage。关键函数/方法:mailjetApiRequest、mailjetApiRequestAllItems、validateJSON。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Mailjet/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Mailjet/GenericFunctions.py

import type {
	IExecuteFunctions,
	ILoadOptionsFunctions,
	IDataObject,
	IHookFunctions,
	IHttpRequestMethods,
	IRequestOptions,
} from 'n8n-workflow';

export async function mailjetApiRequest(
	this: IExecuteFunctions | IHookFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	path: string,

	body: any = {},
	qs: IDataObject = {},
	uri?: string,
	option: IDataObject = {},
): Promise<any> {
	const resource = this.getNodeParameter('resource', 0);

	let credentialType;

	if (resource === 'email' || this.getNode().type.includes('Trigger')) {
		credentialType = 'mailjetEmailApi';
		const { sandboxMode } = await this.getCredentials<{
			sandboxMode: boolean;
		}>('mailjetEmailApi');

		if (!this.getNode().type.includes('Trigger')) {
			Object.assign(body, { SandboxMode: sandboxMode });
		}
	} else {
		credentialType = 'mailjetSmsApi';
	}

	let options: IRequestOptions = {
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
		},
		method,
		qs,
		body,
		uri: uri || `https://api.mailjet.com${path}`,
		json: true,
	};
	options = Object.assign({}, options, option);
	if (Object.keys(options.body as IDataObject).length === 0) {
		delete options.body;
	}

	return await this.helpers.requestWithAuthentication.call(this, credentialType, options);
}

export async function mailjetApiRequestAllItems(
	this: IExecuteFunctions | IHookFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,

	body: any = {},
	query: IDataObject = {},
): Promise<any> {
	const returnData: IDataObject[] = [];

	let responseData;

	query.Limit = 1000;
	query.Offset = 0;

	do {
		responseData = await mailjetApiRequest.call(this, method, endpoint, body, query, undefined, {
			resolveWithFullResponse: true,
		});
		returnData.push.apply(returnData, responseData.body as IDataObject[]);
		query.Offset = query.Offset + query.Limit;
	} while (responseData.length !== 0);
	return returnData;
}

export function validateJSON(json: string | undefined): IDataObject | undefined {
	let result;
	try {
		result = JSON.parse(json!);
	} catch (exception) {
		result = undefined;
	}
	return result;
}

export interface IMessage {
	From?: { Email?: string; Name?: string };
	Subject?: string;
	To?: IDataObject[];
	Cc?: IDataObject[];
	Bcc?: IDataObject[];
	Variables?: IDataObject;
	TemplateLanguage?: boolean;
	TemplateID?: number;
	HTMLPart?: string;
	TextPart?: string;
	TrackOpens?: string;
	ReplyTo?: IDataObject;
	TrackClicks?: string;
	Priority?: number;
	CustomCampaign?: string;
	DeduplicateCampaign?: boolean;
}
