"""
MIGRATION-META:
  source_path: packages/testing/containers/services/redis.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/containers/services 的服务。导入/依赖:外部:@testcontainers/redis、testcontainers；内部:无；本地:../test-containers、./types。导出:RedisMeta、RedisResult、redis。关键函数/方法:start、env。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Testing package (containers harness) -> tests/fixtures/containers
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/containers/services/redis.ts -> services/n8n/tests/testing/fixtures/containers/services/redis.py

import { RedisContainer } from '@testcontainers/redis';
import type { StartedNetwork } from 'testcontainers';

import { TEST_CONTAINER_IMAGES } from '../test-containers';
import type { Service, ServiceResult } from './types';

const HOSTNAME = 'redis';

export interface RedisMeta {
	host: string;
	port: number;
}

export type RedisResult = ServiceResult<RedisMeta>;

export const redis: Service<RedisResult> = {
	description: 'Redis',
	shouldStart: (ctx) => ctx.isQueueMode,

	async start(network: StartedNetwork, projectName: string): Promise<RedisResult> {
		const container = await new RedisContainer(TEST_CONTAINER_IMAGES.redis)
			.withNetwork(network)
			.withNetworkAliases(HOSTNAME)
			.withLabels({
				'com.docker.compose.project': projectName,
				'com.docker.compose.service': HOSTNAME,
			})
			.withName(`${projectName}-${HOSTNAME}`)
			.withReuse()
			.start();

		return {
			container,
			meta: {
				host: HOSTNAME,
				port: 6379,
			},
		};
	},

	env(): Record<string, string> {
		return {
			QUEUE_BULL_REDIS_HOST: HOSTNAME,
			QUEUE_BULL_REDIS_PORT: '6379',
			N8N_CACHE_ENABLED: 'true',
			N8N_CACHE_BACKEND: 'redis',
			N8N_CACHE_REDIS_HOST: HOSTNAME,
			N8N_CACHE_REDIS_PORT: '6379',
		};
	},
};
