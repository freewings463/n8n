"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/MQTT/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/MQTT 的节点。导入/依赖:外部:mqtt、@utils/utilities；内部:n8n-workflow；本地:无。导出:MqttCredential、createClient。关键函数/方法:createClient、onConnect、resolve、onError、reject。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/MQTT/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/MQTT/GenericFunctions.py

import { connect, type IClientOptions, type MqttClient } from 'mqtt';
import { ApplicationError, randomString } from 'n8n-workflow';

import { formatPrivateKey } from '@utils/utilities';

interface BaseMqttCredential {
	protocol: 'mqtt' | 'mqtts' | 'ws';
	host: string;
	port: number;
	username: string;
	password: string;
	clean: boolean;
	clientId: string;
	passwordless?: boolean;
}

type NonSslMqttCredential = BaseMqttCredential & {
	ssl: false;
};

type SslMqttCredential = BaseMqttCredential & {
	ssl: true;
	ca: string;
	cert: string;
	key: string;
	rejectUnauthorized?: boolean;
};
export type MqttCredential = NonSslMqttCredential | SslMqttCredential;

export const createClient = async (credentials: MqttCredential): Promise<MqttClient> => {
	const { protocol, host, port, clean, clientId, username, password } = credentials;

	const clientOptions: IClientOptions = {
		protocol,
		host,
		port,
		clean,
		clientId: clientId || `mqttjs_${randomString(8).toLowerCase()}`,
	};

	if (username && password) {
		clientOptions.username = username;
		clientOptions.password = password;
	}

	if (credentials.ssl) {
		clientOptions.ca = formatPrivateKey(credentials.ca);
		clientOptions.cert = formatPrivateKey(credentials.cert);
		clientOptions.key = formatPrivateKey(credentials.key);
		clientOptions.rejectUnauthorized = credentials.rejectUnauthorized;
	}

	return await new Promise((resolve, reject) => {
		const client = connect(clientOptions);

		const onConnect = () => {
			client.removeListener('connect', onConnect);

			client.removeListener('error', onError);
			resolve(client);
		};

		const onError = (error: Error) => {
			client.removeListener('connect', onConnect);
			client.removeListener('error', onError);
			// mqtt client has an automatic reconnect mechanism that will
			// keep trying to reconnect until it succeeds unless we
			// explicitly close the client
			client.end();
			reject(new ApplicationError(error.message));
		};

		client.once('connect', onConnect);
		client.once('error', onError);
	});
};
