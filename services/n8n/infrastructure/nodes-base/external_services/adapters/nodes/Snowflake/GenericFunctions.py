"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Snowflake/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Snowflake 的节点。导入/依赖:外部:lodash/pick、snowflake-sdk、@utils/utilities；内部:无；本地:无。导出:SnowflakeCredential、getConnectionOptions。关键函数/方法:execute、extractPrivateKey、getConnectionOptions、connect、destroy。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Snowflake/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Snowflake/GenericFunctions.py

import { createPrivateKey } from 'crypto';
import pick from 'lodash/pick';
import type snowflake from 'snowflake-sdk';

import { formatPrivateKey } from '@utils/utilities';

const commonConnectionFields = [
	'account',
	'database',
	'schema',
	'warehouse',
	'role',
	'clientSessionKeepAlive',
] as const;

export type SnowflakeCredential = Pick<
	snowflake.ConnectionOptions,
	(typeof commonConnectionFields)[number]
> &
	(
		| {
				authentication: 'password';
				username?: string;
				password?: string;
		  }
		| {
				authentication: 'keyPair';
				username: string;
				privateKey: string;
				passphrase?: string;
		  }
	);

const extractPrivateKey = (credential: { privateKey: string; passphrase?: string }) => {
	const key = formatPrivateKey(credential.privateKey);

	if (!credential.passphrase) return key;

	const privateKeyObject = createPrivateKey({
		key,
		format: 'pem',
		passphrase: credential.passphrase,
	});

	return privateKeyObject.export({
		format: 'pem',
		type: 'pkcs8',
	}) as string;
};

export const getConnectionOptions = (credential: SnowflakeCredential) => {
	const connectionOptions: snowflake.ConnectionOptions = pick(credential, commonConnectionFields);
	if (credential.authentication === 'keyPair') {
		connectionOptions.authenticator = 'SNOWFLAKE_JWT';
		connectionOptions.username = credential.username;
		connectionOptions.privateKey = extractPrivateKey(credential);
	} else {
		connectionOptions.username = credential.username;
		connectionOptions.password = credential.password;
	}
	return connectionOptions;
};

export async function connect(conn: snowflake.Connection) {
	return await new Promise<void>((resolve, reject) => {
		conn.connect((error) => (error ? reject(error) : resolve()));
	});
}

export async function destroy(conn: snowflake.Connection) {
	return await new Promise<void>((resolve, reject) => {
		conn.destroy((error) => (error ? reject(error) : resolve()));
	});
}

export async function execute(
	conn: snowflake.Connection,
	sqlText: string,
	binds: snowflake.InsertBinds,
) {
	return await new Promise<any[] | undefined>((resolve, reject) => {
		conn.execute({
			sqlText,
			binds,
			complete: (error, _, rows) => (error ? reject(error) : resolve(rows)),
		});
	});
}
