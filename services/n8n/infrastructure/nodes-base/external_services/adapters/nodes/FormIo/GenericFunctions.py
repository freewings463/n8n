"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/FormIo/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/FormIo 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:formIoApiRequest。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/FormIo/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/FormIo/GenericFunctions.py

import type {
	IHookFunctions,
	IHttpRequestMethods,
	IHttpRequestOptions,
	ILoadOptionsFunctions,
	IWebhookFunctions,
	JsonObject,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

interface IFormIoCredentials {
	environment: 'cloudHosted' | ' selfHosted';
	domain?: string;
	email: string;
	password: string;
}

/**
 * Method will call register or list webhooks based on the passed method in the parameter
 */
export async function formIoApiRequest(
	this: IHookFunctions | ILoadOptionsFunctions | IWebhookFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body = {},
	qs = {},
): Promise<any> {
	const credentials = await this.getCredentials<IFormIoCredentials>('formIoApi');

	const base = credentials.domain || 'https://api.form.io';

	const options: IHttpRequestOptions = {
		headers: {
			'Content-Type': 'application/json',
		},
		method,
		body,
		qs,
		url: `${base}${endpoint}`,
		json: true,
	};

	try {
		return await this.helpers.httpRequestWithAuthentication.call(this, 'formIoApi', options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}
