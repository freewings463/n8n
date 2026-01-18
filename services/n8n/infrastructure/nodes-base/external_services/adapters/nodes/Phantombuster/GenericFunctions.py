"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Phantombuster/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Phantombuster 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:validateJSON。关键函数/方法:phantombusterApiRequest、validateJSON。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Phantombuster/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Phantombuster/GenericFunctions.py

import type {
	JsonObject,
	IDataObject,
	IExecuteFunctions,
	ILoadOptionsFunctions,
	IHttpRequestMethods,
	IRequestOptions,
} from 'n8n-workflow';
import { NodeApiError, NodeOperationError } from 'n8n-workflow';

export async function phantombusterApiRequest(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	path: string,

	body: any = {},
	qs: IDataObject = {},
	_option = {},
): Promise<any> {
	const options: IRequestOptions = {
		headers: {},
		method,
		body,
		qs,
		uri: `https://api.phantombuster.com/api/v2${path}`,
		json: true,
	};
	try {
		if (Object.keys(body as IDataObject).length === 0) {
			delete options.body;
		}
		return await this.helpers.requestWithAuthentication.call(this, 'phantombusterApi', options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export function validateJSON(self: IExecuteFunctions, json: string | undefined, name: string) {
	let result;
	try {
		result = JSON.parse(json!);
	} catch (exception) {
		throw new NodeOperationError(self.getNode(), `${name} must provide a valid JSON`);
	}
	return result;
}
