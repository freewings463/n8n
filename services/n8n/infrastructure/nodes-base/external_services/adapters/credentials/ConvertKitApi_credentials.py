"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/ConvertKitApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:无；本地:./common/http。导出:ConvertKitApi。关键函数/方法:authenticate。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/ConvertKitApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/ConvertKitApi_credentials.py

import type {
	ICredentialDataDecryptedObject,
	ICredentialTestRequest,
	ICredentialType,
	IHttpRequestOptions,
	INodeProperties,
} from 'n8n-workflow';
import { getUrl } from './common/http';

export class ConvertKitApi implements ICredentialType {
	name = 'convertKitApi';

	displayName = 'ConvertKit API';

	documentationUrl = 'convertkit';

	properties: INodeProperties[] = [
		{
			displayName: 'API Secret',
			name: 'apiSecret',
			type: 'string',
			default: '',
			typeOptions: {
				password: true,
			},
		},
	];

	async authenticate(credentials: ICredentialDataDecryptedObject, options: IHttpRequestOptions) {
		const url = getUrl(options);
		const secret = {
			api_secret: credentials.apiSecret as string,
		};
		// it's a webhook so include the api secret on the body
		if (url?.includes('/automations/hooks')) {
			options.body = options.body || {};
			if (typeof options.body === 'object') {
				Object.assign(options.body, secret);
			}
		} else {
			options.qs = options.qs || {};
			if (typeof options.qs === 'object') {
				Object.assign(options.qs, secret);
			}
		}
		return options;
	}

	test: ICredentialTestRequest = {
		request: {
			url: 'https://api.convertkit.com/v3/account',
		},
	};
}
