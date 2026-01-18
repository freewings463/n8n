"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/SharePoint/transport/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/SharePoint 的入口。导入/依赖:外部:无；内部:无；本地:无。导出:无。关键函数/方法:microsoftSharePointApiRequest。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/SharePoint/transport/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/SharePoint/transport/__init__.py

import type {
	IDataObject,
	IExecuteFunctions,
	IExecuteSingleFunctions,
	IHttpRequestMethods,
	IHttpRequestOptions,
	ILoadOptionsFunctions,
} from 'n8n-workflow';

export async function microsoftSharePointApiRequest(
	this: IExecuteFunctions | IExecuteSingleFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject | Buffer = {},
	qs?: IDataObject,
	headers?: IDataObject,
	url?: string,
): Promise<any> {
	const credentials: { subdomain: string } = await this.getCredentials(
		'microsoftSharePointOAuth2Api',
	);

	const options: IHttpRequestOptions = {
		method,
		url: url ?? `https://${credentials.subdomain}.sharepoint.com/_api/v2.0${endpoint}`,
		json: true,
		headers,
		body,
		qs,
	};

	return await this.helpers.httpRequestWithAuthentication.call(
		this,
		'microsoftSharePointOAuth2Api',
		options,
	);
}
