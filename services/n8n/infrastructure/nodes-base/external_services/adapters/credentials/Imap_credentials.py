"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/Imap.credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials 的凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:Imap、ICredentialsDataImap、isCredentialsDataImap。关键函数/方法:isCredentialsDataImap。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/Imap.credentials.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/Imap_credentials.py

import type { ICredentialType, INodeProperties } from 'n8n-workflow';

export class Imap implements ICredentialType {
	name = 'imap';

	displayName = 'IMAP';

	documentationUrl = 'imap';

	properties: INodeProperties[] = [
		{
			displayName: 'User',
			name: 'user',
			type: 'string',
			default: '',
		},
		{
			displayName: 'Password',
			name: 'password',
			type: 'string',
			typeOptions: {
				password: true,
			},
			default: '',
		},
		{
			displayName: 'Host',
			name: 'host',
			type: 'string',
			default: '',
		},
		{
			displayName: 'Port',
			name: 'port',
			type: 'number',
			default: 993,
		},
		{
			displayName: 'SSL/TLS',
			name: 'secure',
			type: 'boolean',
			default: true,
		},
		{
			displayName: 'Allow Self-Signed Certificates',
			name: 'allowUnauthorizedCerts',
			type: 'boolean',
			description: 'Whether to connect even if SSL certificate validation is not possible',
			default: false,
		},
	];
}

export interface ICredentialsDataImap {
	host: string;
	port: number;
	user: string;
	password: string;
	secure: boolean;
	allowUnauthorizedCerts: boolean;
}

export function isCredentialsDataImap(candidate: unknown): candidate is ICredentialsDataImap {
	const o = candidate as ICredentialsDataImap;
	return (
		o.host !== undefined &&
		o.password !== undefined &&
		o.port !== undefined &&
		o.secure !== undefined &&
		o.user !== undefined
	);
}
