"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Aws/IAM/transport/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Aws/IAM 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:../helpers/constants。导出:无。关键函数/方法:awsApiRequest、response、statusCode。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Aws/IAM/transport/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Aws/IAM/transport/__init__.py

import type {
	IExecuteSingleFunctions,
	IDataObject,
	IHttpRequestOptions,
	ILoadOptionsFunctions,
	IPollFunctions,
	JsonObject,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

import { BASE_URL } from '../helpers/constants';

const errorMapping: IDataObject = {
	403: 'The AWS credentials are not valid!',
};

export async function awsApiRequest(
	this: ILoadOptionsFunctions | IPollFunctions | IExecuteSingleFunctions,
	opts: IHttpRequestOptions,
): Promise<IDataObject> {
	const requestOptions: IHttpRequestOptions = {
		baseURL: BASE_URL,
		json: true,
		...opts,
		headers: {
			'Content-Type': 'application/x-www-form-urlencoded',
			...(opts.headers ?? {}),
		},
	};

	if (opts.body) {
		requestOptions.body = new URLSearchParams(opts.body as Record<string, string>).toString();
	}

	try {
		const response = (await this.helpers.requestWithAuthentication.call(
			this,
			'aws',
			requestOptions,
		)) as IDataObject;

		return response;
	} catch (error) {
		const statusCode = (error?.statusCode || error?.cause?.statusCode) as string;

		if (statusCode && errorMapping[statusCode]) {
			throw new NodeApiError(this.getNode(), {
				message: `AWS error response [${statusCode}]: ${errorMapping[statusCode] as string}`,
			});
		} else {
			throw new NodeApiError(this.getNode(), error as JsonObject);
		}
	}
}
