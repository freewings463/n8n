"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Signl4/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Signl4 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:SIGNL4ApiRequest。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Signl4/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Signl4/GenericFunctions.py

import type {
	IExecuteFunctions,
	IDataObject,
	JsonObject,
	IRequestOptions,
	IHttpRequestMethods,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

/**
 * Make an API request to SIGNL4
 *
 * @param {IHookFunctions | IExecuteFunctions} this
 *
 */

export async function SIGNL4ApiRequest(
	this: IExecuteFunctions,
	method: IHttpRequestMethods,
	body: string,
	query: IDataObject = {},
	option: IDataObject = {},
): Promise<any> {
	const credentials = await this.getCredentials('signl4Api');

	const teamSecret = credentials?.teamSecret as string;

	let options: IRequestOptions = {
		headers: {
			Accept: '*/*',
		},
		method,
		body,
		qs: query,
		uri: `https://connect.signl4.com/webhook/${teamSecret}`,
		json: true,
	};

	if (!Object.keys(body).length) {
		delete options.body;
	}
	if (!Object.keys(query).length) {
		delete options.qs;
	}
	options = Object.assign({}, options, option);

	try {
		return await this.helpers.request(options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}
