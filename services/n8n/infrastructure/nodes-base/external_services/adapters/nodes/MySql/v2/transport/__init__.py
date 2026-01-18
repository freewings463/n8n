"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/MySql/v2/transport/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/MySql/v2 的入口。导入/依赖:外部:mysql2/promise、node:net、@utils/constants、@utils/utilities；内部:无；本地:../helpers/interfaces。导出:无。关键函数/方法:createPool、resolve。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/MySql/v2/transport/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/MySql/v2/transport/__init__.py

import mysql2 from 'mysql2/promise';
import type {
	ICredentialTestFunctions,
	IDataObject,
	IExecuteFunctions,
	ILoadOptionsFunctions,
} from 'n8n-workflow';
import { createServer, type AddressInfo } from 'node:net';

import { LOCALHOST } from '@utils/constants';
import { formatPrivateKey } from '@utils/utilities';

import type { Mysql2Pool, MysqlNodeCredentials } from '../helpers/interfaces';

export async function createPool(
	this: IExecuteFunctions | ICredentialTestFunctions | ILoadOptionsFunctions,
	credentials: MysqlNodeCredentials,
	options?: IDataObject,
): Promise<Mysql2Pool> {
	const connectionOptions: mysql2.ConnectionOptions = {
		host: credentials.host,
		port: credentials.port,
		database: credentials.database,
		user: credentials.user,
		password: credentials.password,
		multipleStatements: true,
		supportBigNumbers: true,
		decimalNumbers: false,
	};

	if (credentials.ssl) {
		connectionOptions.ssl = {};

		if (credentials.caCertificate) {
			connectionOptions.ssl.ca = formatPrivateKey(credentials.caCertificate);
		}

		if (credentials.clientCertificate || credentials.clientPrivateKey) {
			connectionOptions.ssl.cert = formatPrivateKey(credentials.clientCertificate);
			connectionOptions.ssl.key = formatPrivateKey(credentials.clientPrivateKey);
		}
	}

	if (options?.nodeVersion && (options.nodeVersion as number) >= 2.1) {
		connectionOptions.dateStrings = true;
	}

	if (options?.connectionLimit) {
		connectionOptions.connectionLimit = options.connectionLimit as number;
	}

	if (options?.connectTimeout) {
		connectionOptions.connectTimeout = options.connectTimeout as number;
	}

	if (options?.largeNumbersOutput === 'text') {
		connectionOptions.bigNumberStrings = true;
	}

	if (options?.decimalNumbers === true) {
		connectionOptions.decimalNumbers = true;
	}

	if (!credentials.sshTunnel) {
		return mysql2.createPool(connectionOptions);
	} else {
		if (credentials.sshAuthenticateWith === 'privateKey' && credentials.privateKey) {
			credentials.privateKey = formatPrivateKey(credentials.privateKey);
		}
		const sshClient = await this.helpers.getSSHClient(credentials);

		// Find a free TCP port
		const localPort = await new Promise<number>((resolve) => {
			const tempServer = createServer();
			tempServer.listen(0, LOCALHOST, () => {
				resolve((tempServer.address() as AddressInfo).port);
				tempServer.close();
			});
		});

		const stream = await new Promise((resolve, reject) => {
			sshClient.forwardOut(
				LOCALHOST,
				localPort,
				credentials.host,
				credentials.port,
				(err, clientChannel) => {
					if (err) return reject(err);
					resolve(clientChannel);
				},
			);
		});

		return mysql2.createPool({
			...connectionOptions,
			stream,
		});
	}
}
