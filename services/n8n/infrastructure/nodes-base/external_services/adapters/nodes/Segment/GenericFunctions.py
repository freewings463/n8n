"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Segment/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Segment 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:无。关键函数/方法:segmentApiRequest。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Segment/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Segment/GenericFunctions.py

import type {
	IDataObject,
	IExecuteFunctions,
	IHookFunctions,
	IHttpRequestMethods,
	ILoadOptionsFunctions,
	IRequestOptions,
	IWebhookFunctions,
} from 'n8n-workflow';

export async function segmentApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions | IWebhookFunctions,
	method: IHttpRequestMethods,
	resource: string,
	body: any = {},
	qs: IDataObject = {},
	uri?: string,
	_option: IDataObject = {},
): Promise<any> {
	const options: IRequestOptions = {
		headers: {
			'Content-Type': 'application/json',
		},
		method,
		qs,
		body,
		uri: uri || `https://api.segment.io/v1${resource}`,
		json: true,
	};
	if (!Object.keys(body as IDataObject).length) {
		delete options.body;
	}
	return await this.helpers.requestWithAuthentication.call(this, 'segmentApi', options);
}
