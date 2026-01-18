"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Toggl/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Toggl 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:togglApiRequest。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Toggl/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Toggl/GenericFunctions.py

import type {
	IDataObject,
	IExecuteFunctions,
	IHookFunctions,
	IHttpRequestMethods,
	ILoadOptionsFunctions,
	IPollFunctions,
	IRequestOptions,
	ITriggerFunctions,
	JsonObject,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

export async function togglApiRequest(
	this:
		| ITriggerFunctions
		| IPollFunctions
		| IHookFunctions
		| IExecuteFunctions
		| ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	resource: string,
	body: IDataObject = {},
	query?: IDataObject,
	uri?: string,
) {
	const options: IRequestOptions = {
		method,
		qs: query,
		uri: uri || `https://api.track.toggl.com/api/v9/me${resource}`,
		body,
		json: true,
	};
	if (Object.keys(options.body as IDataObject).length === 0) {
		delete options.body;
	}
	try {
		return await this.helpers.requestWithAuthentication.call(this, 'togglApi', options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}
