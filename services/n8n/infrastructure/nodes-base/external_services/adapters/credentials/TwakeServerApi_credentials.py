"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/TwakeServerApi.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:TwakeServerApi。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/TwakeServerApi.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/TwakeServerApi_credentials.py

import type { ICredentialType, INodeProperties, Icon } from 'n8n-workflow';

export class TwakeServerApi implements ICredentialType {
	name = 'twakeServerApi';

	displayName = 'Twake Server API';

	icon: Icon = 'file:icons/Twake.png';

	documentationUrl = 'twake';

	httpRequestNode = {
		name: 'Twake Server',
		docsUrl: 'https://doc.twake.app/developers-api/home',
		apiBaseUrl: '',
	};

	properties: INodeProperties[] = [
		{
			displayName: 'Host URL',
			name: 'hostUrl',
			type: 'string',
			default: '',
		},
		{
			displayName: 'Public ID',
			name: 'publicId',
			type: 'string',
			default: '',
		},
		{
			displayName: 'Private API Key',
			name: 'privateApiKey',
			type: 'string',
			typeOptions: { password: true },
			default: '',
		},
	];
}
