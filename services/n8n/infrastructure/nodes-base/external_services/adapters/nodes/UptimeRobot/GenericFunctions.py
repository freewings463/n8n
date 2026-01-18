"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/UptimeRobot/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/UptimeRobot 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:uptimeRobotApiRequest。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/UptimeRobot/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/UptimeRobot/GenericFunctions.py

import type {
	IExecuteFunctions,
	IDataObject,
	JsonObject,
	IHttpRequestMethods,
	IRequestOptions,
} from 'n8n-workflow';
import { NodeApiError, NodeOperationError } from 'n8n-workflow';

export async function uptimeRobotApiRequest(
	this: IExecuteFunctions,
	method: IHttpRequestMethods,
	resource: string,
	body: IDataObject = {},
	qs: IDataObject = {},
	uri?: string,
	option: IDataObject = {},
) {
	const credentials = await this.getCredentials('uptimeRobotApi');

	let options: IRequestOptions = {
		method,
		qs,
		form: {
			api_key: credentials.apiKey,
			...body,
		},
		uri: uri || `https://api.uptimerobot.com/v2${resource}`,
		json: true,
	};
	options = Object.assign({}, options, option);
	try {
		const responseData = await this.helpers.request(options);
		if (responseData.stat !== 'ok') {
			throw new NodeOperationError(this.getNode(), responseData as Error);
		}
		return responseData;
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}
