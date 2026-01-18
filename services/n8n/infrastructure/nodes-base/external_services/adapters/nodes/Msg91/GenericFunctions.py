"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Msg91/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Msg91 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:msg91ApiRequest。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Msg91/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Msg91/GenericFunctions.py

import type {
	IExecuteFunctions,
	IHookFunctions,
	IDataObject,
	JsonObject,
	IHttpRequestMethods,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

/**
 * Make an API request to MSG91
 *
 */
export async function msg91ApiRequest(
	this: IHookFunctions | IExecuteFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject,
	query?: IDataObject,
): Promise<any> {
	const credentials = await this.getCredentials('msg91Api');

	if (query === undefined) {
		query = {};
	}

	query.authkey = credentials.authkey as string;

	const options = {
		method,
		form: body,
		qs: query,
		uri: `https://api.msg91.com/api${endpoint}`,
		json: true,
	};

	try {
		return await this.helpers.request(options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}
