"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Twake/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Twake 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:无。关键函数/方法:twakeApiRequest。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Twake/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Twake/GenericFunctions.py

import type {
	IDataObject,
	IExecuteFunctions,
	IHookFunctions,
	IHttpRequestMethods,
	ILoadOptionsFunctions,
	IRequestOptions,
} from 'n8n-workflow';

/**
 * Make an API request to Twake
 *
 */
export async function twakeApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	resource: string,
	body: object,
	query?: IDataObject,
	uri?: string,
) {
	const options: IRequestOptions = {
		headers: {},
		method,
		body,
		qs: query,
		uri: uri || `https://plugins.twake.app/plugins/n8n${resource}`,
		json: true,
	};

	// if (authenticationMethod === 'cloud') {
	// } else {
	// 	const credentials = await this.getCredentials('twakeServerApi');
	// 	options.auth = { user: credentials!.publicId as string, pass: credentials!.privateApiKey as string };
	// 	options.uri = `${credentials!.hostUrl}/api/v1${resource}`;
	// }

	return await this.helpers.requestWithAuthentication.call(this, 'twakeCloudApi', options);
}
