"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Postgres/v2/methods/listSearch.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Postgres/v2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../../transport、../helpers/interfaces。导出:无。关键函数/方法:schemaSearch、tableSearch。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Postgres/v2/methods/listSearch.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Postgres/v2/methods/listSearch.py

import type { ILoadOptionsFunctions, INodeListSearchResult } from 'n8n-workflow';

import { configurePostgres } from '../../transport';
import type { PostgresNodeCredentials } from '../helpers/interfaces';

export async function schemaSearch(this: ILoadOptionsFunctions): Promise<INodeListSearchResult> {
	const credentials = await this.getCredentials<PostgresNodeCredentials>('postgres');
	const options = { nodeVersion: this.getNode().typeVersion };

	const { db } = await configurePostgres.call(this, credentials, options);

	const response = await db.any('SELECT schema_name FROM information_schema.schemata');

	return {
		results: response.map((schema) => ({
			name: schema.schema_name as string,
			value: schema.schema_name as string,
		})),
	};
}
export async function tableSearch(this: ILoadOptionsFunctions): Promise<INodeListSearchResult> {
	const credentials = await this.getCredentials<PostgresNodeCredentials>('postgres');
	const options = { nodeVersion: this.getNode().typeVersion };

	const { db } = await configurePostgres.call(this, credentials, options);

	const schema = this.getNodeParameter('schema', 0, {
		extractValue: true,
	}) as string;

	const response = await db.any(
		'SELECT table_name FROM information_schema.tables WHERE table_schema=$1',
		[schema],
	);

	return {
		results: response.map((table) => ({
			name: table.table_name as string,
			value: table.table_name as string,
		})),
	};
}
