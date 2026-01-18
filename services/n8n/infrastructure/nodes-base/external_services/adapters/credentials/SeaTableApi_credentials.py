"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/SeaTableApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:moment-timezone；内部:无；本地:无。导出:SeaTableApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/SeaTableApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/SeaTableApi_credentials.py

import moment from 'moment-timezone';
import type {
	ICredentialTestRequest,
	ICredentialType,
	INodeProperties,
	INodePropertyOptions,
} from 'n8n-workflow';

// Get options for timezones
const timezones: INodePropertyOptions[] = moment.tz
	.countries()
	.reduce((tz: INodePropertyOptions[], country: string) => {
		const zonesForCountry = moment.tz
			.zonesForCountry(country)
			.map((zone) => ({ value: zone, name: zone }));
		return tz.concat(zonesForCountry);
	}, []);

export class SeaTableApi implements ICredentialType {
	name = 'seaTableApi';

	displayName = 'SeaTable API';

	documentationUrl = 'seatable';

	properties: INodeProperties[] = [
		{
			displayName: 'Environment',
			name: 'environment',
			type: 'options',
			default: 'cloudHosted',
			options: [
				{
					name: 'Cloud-Hosted',
					value: 'cloudHosted',
				},
				{
					name: 'Self-Hosted',
					value: 'selfHosted',
				},
			],
		},
		{
			displayName: 'Self-Hosted Domain',
			name: 'domain',
			type: 'string',
			default: '',
			placeholder: 'https://seatable.example.com',
			displayOptions: {
				show: {
					environment: ['selfHosted'],
				},
			},
		},
		{
			displayName: 'API Token (of a Base)',
			name: 'token',
			type: 'string',
			description:
				'The API-Token of the SeaTable base you would like to use with n8n. n8n can only connect to one base at a time.',
			typeOptions: { password: true },
			default: '',
		},
		{
			displayName: 'Timezone',
			name: 'timezone',
			type: 'options',
			default: '',
			description: "Seatable server's timezone",
			options: [...timezones],
		},
	];

	test: ICredentialTestRequest = {
		request: {
			baseURL: '={{$credentials?.domain || "https://cloud.seatable.io" }}',
			url: '/api/v2.1/dtable/app-access-token/',
			headers: {
				Authorization: '={{"Token " + $credentials.token}}',
			},
		},
	};
}
