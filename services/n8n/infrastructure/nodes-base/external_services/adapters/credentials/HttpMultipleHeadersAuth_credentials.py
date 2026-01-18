"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/HttpMultipleHeadersAuth.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:HttpMultipleHeadersAuth。关键函数/方法:values。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。注释目标:eslint-disable n8n-nodes-base/cred-class-name-unsuffixed。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/HttpMultipleHeadersAuth.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/HttpMultipleHeadersAuth_credentials.py

/* eslint-disable n8n-nodes-base/cred-class-name-unsuffixed */
/* eslint-disable n8n-nodes-base/cred-class-field-name-unsuffixed */
import type { IAuthenticate, ICredentialType, INodeProperties, Icon } from 'n8n-workflow';

export class HttpMultipleHeadersAuth implements ICredentialType {
	name = 'httpMultipleHeadersAuth';

	displayName = 'Multiple Headers Auth';

	documentationUrl = 'httprequest';

	icon: Icon = 'node:n8n-nodes-base.httpRequest';

	properties: INodeProperties[] = [
		{
			displayName: 'Headers',
			name: 'headers',
			type: 'fixedCollection',
			default: { values: [{ name: '', value: '' }] },
			typeOptions: {
				multipleValues: true,
			},
			placeholder: 'Add Header',
			options: [
				{
					displayName: 'Header',
					name: 'values',
					values: [
						{
							displayName: 'Name',
							name: 'name',
							type: 'string',
							default: '',
						},
						{
							displayName: 'Value',
							name: 'value',
							type: 'string',
							default: '',
							typeOptions: {
								password: true,
							},
						},
					],
				},
			],
		},
	];

	authenticate: IAuthenticate = async (credentials, requestOptions) => {
		const values = (credentials.headers as { values: Array<{ name: string; value: string }> })
			.values;
		const headers = values.reduce(
			(acc, cur) => {
				acc[cur.name] = cur.value;
				return acc;
			},
			{} as Record<string, string>,
		);
		const newRequestOptions = {
			...requestOptions,
			headers: {
				...requestOptions.headers,
				...headers,
			},
		};
		return await Promise.resolve(newRequestOptions);
	};
}
