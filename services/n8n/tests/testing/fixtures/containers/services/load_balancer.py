"""
MIGRATION-META:
  source_path: packages/testing/containers/services/load-balancer.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/containers/services 的服务。导入/依赖:外部:testcontainers；内部:无；本地:../helpers/utils、../test-containers、./types。导出:LoadBalancerConfig、LoadBalancerMeta、LoadBalancerResult、loadBalancer。关键函数/方法:start、buildCaddyConfig、getOptions、env。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Testing package (containers harness) -> tests/fixtures/containers
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/containers/services/load-balancer.ts -> services/n8n/tests/testing/fixtures/containers/services/load_balancer.py

import { GenericContainer, Wait } from 'testcontainers';

import { createSilentLogConsumer } from '../helpers/utils';
import { TEST_CONTAINER_IMAGES } from '../test-containers';
import type { Service, ServiceResult } from './types';

export interface LoadBalancerConfig {
	mainCount: number;
	hostPort?: number;
}

export interface LoadBalancerMeta {
	hostPort: number;
	baseUrl: string;
}

export type LoadBalancerResult = ServiceResult<LoadBalancerMeta>;

function buildCaddyConfig(upstreamServers: string[]): string {
	const backends = upstreamServers.join(' ');
	return `
:80 {
  # Reverse proxy with load balancing
  reverse_proxy ${backends} {
    # Use first available backend for simpler debugging
    lb_policy first

    # Health check
    health_uri /healthz
    health_interval 10s

    # Timeouts
    transport http {
      dial_timeout 60s
      read_timeout 60s
      write_timeout 60s
    }
  }

  # Set max request body size
  request_body {
    max_size 50MB
  }
}`;
}

export const loadBalancer: Service<LoadBalancerResult> = {
	description: 'Caddy load balancer',
	shouldStart: (ctx) => ctx.needsLoadBalancer,

	getOptions(ctx) {
		return {
			mainCount: ctx.mains,
			hostPort: ctx.allocatedPorts.loadBalancer,
		} as LoadBalancerConfig;
	},

	env(result) {
		return {
			WEBHOOK_URL: result.meta.baseUrl,
			N8N_PROXY_HOPS: '1',
		};
	},

	async start(network, projectName, config?: unknown): Promise<LoadBalancerResult> {
		const { mainCount, hostPort } = config as LoadBalancerConfig;
		const { consumer, throwWithLogs } = createSilentLogConsumer();

		// Generate upstream server addresses
		const upstreamServers = Array.from(
			{ length: mainCount },
			(_, index) => `${projectName}-n8n-main-${index + 1}:5678`,
		);

		const caddyConfig = buildCaddyConfig(upstreamServers);

		try {
			const container = await new GenericContainer(TEST_CONTAINER_IMAGES.caddy)
				.withNetwork(network)
				.withExposedPorts(hostPort ? { container: 80, host: hostPort } : 80)
				.withCopyContentToContainer([{ content: caddyConfig, target: '/etc/caddy/Caddyfile' }])
				.withWaitStrategy(Wait.forListeningPorts())
				.withLabels({
					'com.docker.compose.project': projectName,
					'com.docker.compose.service': 'caddy-lb',
				})
				.withName(`${projectName}-caddy-lb`)
				.withReuse()
				.withLogConsumer(consumer)
				.start();

			const actualHostPort = container.getMappedPort(80);

			return {
				container,
				meta: {
					hostPort: actualHostPort,
					baseUrl: `http://localhost:${actualHostPort}`,
				},
			};
		} catch (error) {
			return throwWithLogs(error);
		}
	},
};
