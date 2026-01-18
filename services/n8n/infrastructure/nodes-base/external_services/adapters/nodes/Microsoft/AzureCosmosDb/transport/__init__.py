"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/AzureCosmosDb/transport/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/AzureCosmosDb 的入口。导入/依赖:外部:无；内部:无；本地:../helpers/interfaces。导出:无。关键函数/方法:azureCosmosDbApiRequest。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/AzureCosmosDb/transport/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/AzureCosmosDb/transport/__init__.py

import type {
	IDataObject,
	IHttpRequestOptions,
	IHttpRequestMethods,
	ILoadOptionsFunctions,
	IExecuteSingleFunctions,
} from 'n8n-workflow';

import type { ICosmosDbCredentials } from '../helpers/interfaces';

export async function azureCosmosDbApiRequest(
	this: IExecuteSingleFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject = {},
	qs?: IDataObject,
	headers?: IDataObject,
	returnFullResponse: boolean = false,
): Promise<any> {
	const credentialsType = 'microsoftAzureCosmosDbSharedKeyApi';
	const credentials = await this.getCredentials<ICosmosDbCredentials>(credentialsType);
	const baseUrl = `https://${credentials.account}.documents.azure.com/dbs/${credentials.database}`;

	const options: IHttpRequestOptions = {
		method,
		url: `${baseUrl}${endpoint}`,
		json: true,
		headers,
		body,
		qs,
		returnFullResponse,
	};

	return await this.helpers.httpRequestWithAuthentication.call(this, credentialsType, options);
}
