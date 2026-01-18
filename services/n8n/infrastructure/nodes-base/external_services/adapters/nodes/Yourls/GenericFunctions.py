"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Yourls/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Yourls 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:yourlsApiRequest。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Yourls/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Yourls/GenericFunctions.py

import type {
	IExecuteFunctions,
	ILoadOptionsFunctions,
	IDataObject,
	JsonObject,
	IHttpRequestMethods,
	IRequestOptions,
} from 'n8n-workflow';
import { NodeApiError, NodeOperationError } from 'n8n-workflow';

export async function yourlsApiRequest(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,

	body: any = {},
	qs: IDataObject = {},
): Promise<any> {
	const credentials = await this.getCredentials('yourlsApi');

	qs.signature = credentials.signature as string;
	qs.format = 'json';

	const options: IRequestOptions = {
		method,
		body,
		qs,
		uri: `${credentials.url}/yourls-api.php`,
		json: true,
	};
	try {
		const response = await this.helpers.request.call(this, options);

		if (response.status === 'fail') {
			throw new NodeOperationError(
				this.getNode(),
				`Yourls error response [400]: ${response.message}`,
			);
		}

		if (typeof response === 'string' && response.includes('<b>Fatal error</b>')) {
			throw new NodeOperationError(
				this.getNode(),
				"Yourls responded with a 'Fatal error', check description for more details",
				{
					description: `Server response:\n${response}`,
				},
			);
		}

		return response;
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}
