"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Lemlist/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Lemlist 的节点。导入/依赖:外部:change-case；内部:无；本地:无。导出:getEvents。关键函数/方法:lemlistApiRequest、lemlistApiRequestAllItems、getEvents。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Lemlist/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Lemlist/GenericFunctions.py

import { capitalCase } from 'change-case';
import type {
	IExecuteFunctions,
	IHookFunctions,
	IDataObject,
	ILoadOptionsFunctions,
	IHttpRequestMethods,
	IRequestOptions,
} from 'n8n-workflow';

/**
 * Make an authenticated API request to Lemlist.
 */
export async function lemlistApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject = {},
	qs: IDataObject = {},
	option: IDataObject = {},
) {
	const options: IRequestOptions = {
		headers: {},
		method,
		uri: `https://api.lemlist.com/api${endpoint}`,
		qs,
		body,
		json: true,
	};

	if (!Object.keys(body).length) {
		delete options.body;
	}

	if (!Object.keys(qs).length) {
		delete options.qs;
	}

	if (Object.keys(option)) {
		Object.assign(options, option);
	}

	return await this.helpers.requestWithAuthentication.call(this, 'lemlistApi', options);
}

/**
 * Make an authenticated API request to Lemlist and return all results.
 */
export async function lemlistApiRequestAllItems(
	this: IExecuteFunctions | ILoadOptionsFunctions | IHookFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	qs: IDataObject = {},
) {
	const returnData: IDataObject[] = [];

	let responseData;

	qs.limit = 100;
	qs.offset = 0;
	//when using v2, the pagination is different
	if (qs.version && qs.version === 'v2') {
		qs.page = 1;
		do {
			responseData = await lemlistApiRequest.call(this, method, endpoint, {}, qs);
			returnData.push(...(responseData as IDataObject[]));
			qs.page++;
		} while (responseData.totalPage && qs.page < responseData.totalPage);
		return returnData;
	} else {
		do {
			responseData = await lemlistApiRequest.call(this, method, endpoint, {}, qs);
			returnData.push(...(responseData as IDataObject[]));
			qs.offset += qs.limit;
		} while (responseData.length !== 0);
		return returnData;
	}
}

export function getEvents() {
	const events = [
		'*',
		'contacted',
		'hooked',
		'attracted',
		'warmed',
		'interested',
		'skipped',
		'notInterested',
		'emailsSent',
		'emailsOpened',
		'emailsClicked',
		'emailsReplied',
		'emailsBounced',
		'emailsSendFailed',
		'emailsFailed',
		'emailsUnsubscribed',
		'emailsInterested',
		'emailsNotInterested',
		'opportunitiesDone',
		'aircallCreated',
		'aircallEnded',
		'aircallDone',
		'aircallInterested',
		'aircallNotInterested',
		'apiDone',
		'apiInterested',
		'apiNotInterested',
		'apiFailed',
		'linkedinVisitDone',
		'linkedinVisitFailed',
		'linkedinInviteDone',
		'linkedinInviteFailed',
		'linkedinInviteAccepted',
		'linkedinReplied',
		'linkedinSent',
		'linkedinVoiceNoteDone',
		'linkedinVoiceNoteFailed',
		'linkedinInterested',
		'linkedinNotInterested',
		'linkedinSendFailed',
		'manualInterested',
		'manualNotInterested',
		'paused',
		'resumed',
		'customDomainErrors',
		'connectionIssue',
		'sendLimitReached',
		'lemwarmPaused',
	];

	return events.map((event: string) => ({
		name: event === '*' ? '*' : capitalCase(event).replace('Linkedin', 'LinkedIn'),
		value: event,
	}));
}
