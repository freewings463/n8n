"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/HumanticAI/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/HumanticAI 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:humanticAiApiRequest。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/HumanticAI/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/HumanticAI/GenericFunctions.py

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

export async function humanticAiApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	resource: string,

	body: any = {},
	qs: IDataObject = {},
	option: IDataObject = {},
): Promise<any> {
	try {
		const credentials = await this.getCredentials('humanticAiApi');
		let options = {
			headers: {
				'Content-Type': 'application/json',
			},
			method,
			qs,
			body,
			uri: `https://api.humantic.ai/v1${resource}`,
			json: true,
		} satisfies IRequestOptions;

		options = Object.assign({}, options, option);
		options.qs.apikey = credentials.apiKey;

		if (Object.keys(options.body as IDataObject).length === 0) {
			delete options.body;
		}

		const response = await this.helpers.request(options);

		if (response.data && response.data.status === 'error') {
			throw new NodeApiError(this.getNode(), response.data as JsonObject);
		}

		return response;
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}
