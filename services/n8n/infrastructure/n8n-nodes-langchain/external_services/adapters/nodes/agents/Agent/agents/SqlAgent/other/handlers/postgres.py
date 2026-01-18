"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/SqlAgent/other/handlers/postgres.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/agents/Agent 的节点。导入/依赖:外部:tls；内部:@n8n/typeorm、n8n-nodes-base/…/interfaces、n8n-workflow；本地:无。导出:无。关键函数/方法:getPostgresDataSource。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/SqlAgent/other/handlers/postgres.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/agents/Agent/agents/SqlAgent/other/handlers/postgres.py

import { DataSource } from '@n8n/typeorm';
import type { PostgresNodeCredentials } from 'n8n-nodes-base/dist/nodes/Postgres/v2/helpers/interfaces';
import { type IExecuteFunctions } from 'n8n-workflow';
import type { TlsOptions } from 'tls';

export async function getPostgresDataSource(this: IExecuteFunctions): Promise<DataSource> {
	const credentials = await this.getCredentials<PostgresNodeCredentials>('postgres');

	let ssl: TlsOptions | boolean = !['disable', undefined].includes(credentials.ssl);
	if (credentials.allowUnauthorizedCerts && ssl) {
		ssl = { rejectUnauthorized: false };
	}

	return new DataSource({
		type: 'postgres',
		host: credentials.host,
		port: credentials.port,
		username: credentials.user,
		password: credentials.password,
		database: credentials.database,
		ssl,
	});
}
