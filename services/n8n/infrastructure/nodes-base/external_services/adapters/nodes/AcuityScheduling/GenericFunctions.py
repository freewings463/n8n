"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/AcuityScheduling/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/AcuityScheduling 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:acuitySchedulingApiRequest。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/AcuityScheduling/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/AcuityScheduling/GenericFunctions.py

import type {
	IDataObject,
	IExecuteFunctions,
	IHookFunctions,
	IHttpRequestMethods,
	ILoadOptionsFunctions,
	IRequestOptions,
	IWebhookFunctions,
	JsonObject,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

export async function acuitySchedulingApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions | IWebhookFunctions,
	method: IHttpRequestMethods,
	resource: string,
	body: any = {},
	qs: IDataObject = {},
	uri?: string,
	_option: IDataObject = {},
): Promise<any> {
	const authenticationMethod = this.getNodeParameter('authentication', 0);

	const options: IRequestOptions = {
		headers: {
			'Content-Type': 'application/json',
		},
		auth: {},
		method,
		qs,
		body,
		uri: uri || `https://acuityscheduling.com/api/v1${resource}`,
		json: true,
	};

	try {
		if (authenticationMethod === 'apiKey') {
			const credentials = await this.getCredentials('acuitySchedulingApi');

			options.auth = {
				user: credentials.userId as string,
				password: credentials.apiKey as string,
			};

			return await this.helpers.request(options);
		} else {
			delete options.auth;
			return await this.helpers.requestOAuth2.call(
				this,
				'acuitySchedulingOAuth2Api',
				options,
				//@ts-ignore
				true,
			);
		}
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}
