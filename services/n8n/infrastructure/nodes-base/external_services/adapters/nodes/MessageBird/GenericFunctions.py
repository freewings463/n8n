"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/MessageBird/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/MessageBird 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:messageBirdApiRequest。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/MessageBird/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/MessageBird/GenericFunctions.py

import type {
	IExecuteFunctions,
	IHookFunctions,
	IDataObject,
	JsonObject,
	IHttpRequestMethods,
	IRequestOptions,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

/**
 * Make an API request to Message Bird
 *
 */
export async function messageBirdApiRequest(
	this: IHookFunctions | IExecuteFunctions,
	method: IHttpRequestMethods,
	resource: string,
	body: IDataObject,
	query: IDataObject = {},
): Promise<any> {
	const credentials = await this.getCredentials('messageBirdApi');

	const options: IRequestOptions = {
		headers: {
			Accept: 'application/json',
			Authorization: `AccessKey ${credentials.accessKey}`,
		},
		method,
		qs: query,
		body,
		uri: `https://rest.messagebird.com${resource}`,
		json: true,
	};
	try {
		if (Object.keys(body).length === 0) {
			delete options.body;
		}
		return await this.helpers.request(options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}
