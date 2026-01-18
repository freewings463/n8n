"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/SqlAgent/other/handlers/mysql.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/agents/Agent 的节点。导入/依赖:外部:无；内部:@n8n/typeorm、n8n-workflow；本地:无。导出:无。关键函数/方法:getMysqlDataSource。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/SqlAgent/other/handlers/mysql.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/agents/Agent/agents/SqlAgent/other/handlers/mysql.py

import { DataSource } from '@n8n/typeorm';
import { type IExecuteFunctions } from 'n8n-workflow';

export async function getMysqlDataSource(this: IExecuteFunctions): Promise<DataSource> {
	const credentials = await this.getCredentials('mySql');

	const dataSource = new DataSource({
		type: 'mysql',
		host: credentials.host as string,
		port: credentials.port as number,
		username: credentials.user as string,
		password: credentials.password as string,
		database: credentials.database as string,
		ssl: {
			rejectUnauthorized: credentials.ssl as boolean,
		},
	});

	return dataSource;
}
