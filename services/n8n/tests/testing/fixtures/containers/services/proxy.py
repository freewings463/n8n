"""
MIGRATION-META:
  source_path: packages/testing/containers/services/proxy.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/containers/services 的服务。导入/依赖:外部:testcontainers；内部:无；本地:../helpers/utils、../test-containers、./types。导出:ProxyMeta、ProxyResult、proxy。关键函数/方法:start、extraEnv、env。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Testing package (containers harness) -> tests/fixtures/containers
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/containers/services/proxy.ts -> services/n8n/tests/testing/fixtures/containers/services/proxy.py

import { GenericContainer, Wait } from 'testcontainers';

import { createSilentLogConsumer } from '../helpers/utils';
import { TEST_CONTAINER_IMAGES } from '../test-containers';
import type { Service, ServiceResult } from './types';

const HOSTNAME = 'proxyserver';
const PORT = 1080;

export interface ProxyMeta {
	host: string;
	port: number;
	internalUrl: string;
}

export type ProxyResult = ServiceResult<ProxyMeta>;

export const proxy: Service<ProxyResult> = {
	description: 'HTTP proxy server',

	extraEnv(result): Record<string, string> {
		return {
			HTTP_PROXY: result.meta.internalUrl,
			HTTPS_PROXY: result.meta.internalUrl,
			NODE_TLS_REJECT_UNAUTHORIZED: '0',
		};
	},

	async start(network, projectName): Promise<ProxyResult> {
		const { consumer, throwWithLogs } = createSilentLogConsumer();

		try {
			const container = await new GenericContainer(TEST_CONTAINER_IMAGES.mockserver)
				.withNetwork(network)
				.withNetworkAliases(HOSTNAME)
				.withExposedPorts(PORT)
				.withWaitStrategy(Wait.forLogMessage(`INFO ${PORT} started on port: ${PORT}`))
				.withLabels({
					'com.docker.compose.project': projectName,
					'com.docker.compose.service': HOSTNAME,
				})
				.withName(`${projectName}-${HOSTNAME}`)
				.withReuse()
				.withLogConsumer(consumer)
				.start();

			return {
				container,
				meta: {
					host: HOSTNAME,
					port: PORT,
					internalUrl: `http://${HOSTNAME}:${PORT}`,
				},
			};
		} catch (error) {
			return throwWithLogs(error);
		}
	},

	env(result): Record<string, string> {
		return {
			N8N_PROXY_HOST: result.meta.host,
			N8N_PROXY_PORT: String(result.meta.port),
		};
	},
};
