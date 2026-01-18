"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Ldap/Helpers.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Ldap 的LDAP工具。导入/依赖:外部:ldapts；内部:n8n-workflow；本地:无。导出:BINARY_AD_ATTRIBUTES、resolveBinaryAttributes。关键函数/方法:resolveEntryBinaryAttributes、resolveBinaryAttributes、createLdapClient。用于提供LDAP通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Ldap/Helpers.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Ldap/Helpers.py

import { Client } from 'ldapts';
import type { ClientOptions, Entry } from 'ldapts';
import type { ICredentialDataDecryptedObject, IDataObject, Logger } from 'n8n-workflow';
export const BINARY_AD_ATTRIBUTES = ['objectGUID', 'objectSid'];

const resolveEntryBinaryAttributes = (entry: Entry): Entry => {
	Object.entries(entry)
		.filter(([k]) => BINARY_AD_ATTRIBUTES.includes(k))
		.forEach(([k]) => {
			entry[k] = (entry[k] as Buffer).toString('hex');
		});
	return entry;
};

export const resolveBinaryAttributes = (entries: Entry[]): void => {
	entries.forEach((entry) => resolveEntryBinaryAttributes(entry));
};

export async function createLdapClient(
	context: { logger: Logger },
	credentials: ICredentialDataDecryptedObject,
	nodeDebug?: boolean,
	nodeType?: string,
	nodeName?: string,
): Promise<Client> {
	const protocol = credentials.connectionSecurity === 'tls' ? 'ldaps' : 'ldap';
	const url = `${protocol}://${credentials.hostname}:${credentials.port}`;

	const ldapOptions: ClientOptions = { url };
	const tlsOptions: IDataObject = {};

	if (credentials.connectionSecurity !== 'none') {
		tlsOptions.rejectUnauthorized = credentials.allowUnauthorizedCerts === false;
		if (credentials.caCertificate) {
			tlsOptions.ca = [credentials.caCertificate as string];
		}
		if (credentials.connectionSecurity !== 'startTls') {
			ldapOptions.tlsOptions = tlsOptions;
		}
	}

	if (credentials.timeout) {
		// Convert seconds to milliseconds
		ldapOptions.timeout = (credentials.timeout as number) * 1000;
	}

	if (nodeDebug) {
		context.logger.info(
			`[${nodeType} | ${nodeName}] - LDAP Options: ${JSON.stringify(ldapOptions, null, 2)}`,
		);
	}

	const client = new Client(ldapOptions);
	if (credentials.connectionSecurity === 'startTls') {
		await client.startTLS(tlsOptions);
	}
	return client;
}
