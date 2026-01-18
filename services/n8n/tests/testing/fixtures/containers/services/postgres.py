"""
MIGRATION-META:
  source_path: packages/testing/containers/services/postgres.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/containers/services 的服务。导入/依赖:外部:@testcontainers/postgresql、testcontainers；内部:无；本地:../test-containers、./types。导出:PostgresMeta、PostgresResult、postgres。关键函数/方法:start、env。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Testing package (containers harness) -> tests/fixtures/containers
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/containers/services/postgres.ts -> services/n8n/tests/testing/fixtures/containers/services/postgres.py

import { PostgreSqlContainer } from '@testcontainers/postgresql';
import type { StartedNetwork } from 'testcontainers';

import { TEST_CONTAINER_IMAGES } from '../test-containers';
import type { Service, ServiceResult } from './types';

const HOSTNAME = 'postgres';

export interface PostgresMeta {
	database: string;
	username: string;
	password: string;
}

export type PostgresResult = ServiceResult<PostgresMeta>;

export const postgres: Service<PostgresResult> = {
	description: 'PostgreSQL database',
	shouldStart: (ctx) => ctx.usePostgres,

	async start(network: StartedNetwork, projectName: string): Promise<PostgresResult> {
		const container = await new PostgreSqlContainer(TEST_CONTAINER_IMAGES.postgres)
			.withNetwork(network)
			.withNetworkAliases(HOSTNAME)
			.withDatabase('n8n_db')
			.withUsername('n8n_user')
			.withPassword('test_password')
			.withStartupTimeout(30000)
			.withLabels({
				'com.docker.compose.project': projectName,
				'com.docker.compose.service': HOSTNAME,
			})
			.withName(`${projectName}-${HOSTNAME}`)
			.withAddedCapabilities('NET_ADMIN') // Allows us to drop IP tables and block traffic
			.withReuse()
			.start();

		return {
			container,
			meta: {
				database: container.getDatabase(),
				username: container.getUsername(),
				password: container.getPassword(),
			},
		};
	},

	env(result: PostgresResult): Record<string, string> {
		return {
			DB_TYPE: 'postgresdb',
			DB_POSTGRESDB_HOST: HOSTNAME,
			DB_POSTGRESDB_PORT: '5432',
			DB_POSTGRESDB_DATABASE: result.meta.database,
			DB_POSTGRESDB_USER: result.meta.username,
			DB_POSTGRESDB_PASSWORD: result.meta.password,
		};
	},
};
