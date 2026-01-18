"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Sms77/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Sms77 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:sms77ApiRequest。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Sms77/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Sms77/GenericFunctions.py

import type {
	IDataObject,
	IExecuteFunctions,
	IHookFunctions,
	IHttpRequestMethods,
	IRequestOptions,
	JsonObject,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

/**
 * Make an API request to seven
 *
 * @param {IHookFunctions | IExecuteFunctions} this
 * @param {object | undefined} data
 */
export async function sms77ApiRequest(
	this: IHookFunctions | IExecuteFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject,
	qs: IDataObject = {},
): Promise<any> {
	const options: IRequestOptions = {
		headers: {
			SentWith: 'n8n',
		},
		qs,
		uri: `https://gateway.seven.io/api${endpoint}`,
		json: true,
		method,
	};

	if (Object.keys(body).length) {
		options.form = body;
	}

	const response = await this.helpers.requestWithAuthentication.call(this, 'sms77Api', options);

	if (response.success !== '100') {
		throw new NodeApiError(this.getNode(), response as JsonObject, {
			message: 'Invalid sms77 credentials or API error!',
		});
	}

	return response;
}
