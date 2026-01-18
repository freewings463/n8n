"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/UProc/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/UProc 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:uprocApiRequest。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/UProc/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/UProc/GenericFunctions.py

import type {
	IDataObject,
	IExecuteFunctions,
	IHookFunctions,
	ILoadOptionsFunctions,
	IHttpRequestMethods,
	IHttpRequestOptions,
	JsonObject,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

export async function uprocApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	body: any = {},
	qs: IDataObject = {},
	_option: IDataObject = {},
): Promise<any> {
	const options: IHttpRequestOptions = {
		method,
		qs,
		body,
		url: 'https://api.uproc.io/api/v2/process',
		json: true,
	};

	try {
		return await this.helpers.httpRequestWithAuthentication.call(this, 'uprocApi', options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}
