"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/MySql/v2/actions/router.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/MySql/v2 的路由。导入/依赖:外部:无；内部:n8n-workflow；本地:./database/Database.resource、./node.type、../utils/utilities、../helpers/interfaces 等2项。导出:无。关键函数/方法:router、addExecutionHints。用于组织该模块路由，绑定控制器与中间件，定义API边界。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/MySql/v2/actions/router.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/MySql/v2/actions/router.py

import type { IExecuteFunctions, INodeExecutionData } from 'n8n-workflow';
import { NodeOperationError } from 'n8n-workflow';

import * as database from './database/Database.resource';
import type { MySqlType } from './node.type';
import { addExecutionHints } from '../../../../utils/utilities';
import type { MysqlNodeCredentials, QueryRunner } from '../helpers/interfaces';
import { configureQueryRunner } from '../helpers/utils';
import { createPool } from '../transport';

export async function router(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
	let returnData: INodeExecutionData[] = [];

	const items = this.getInputData();
	const resource = this.getNodeParameter<MySqlType>('resource', 0);
	const operation = this.getNodeParameter('operation', 0);
	const nodeOptions = this.getNodeParameter('options', 0);
	const node = this.getNode();

	nodeOptions.nodeVersion = node.typeVersion;

	const credentials = await this.getCredentials<MysqlNodeCredentials>('mySql');

	const pool = await createPool.call(this, credentials, nodeOptions);

	const runQueries: QueryRunner = configureQueryRunner.call(this, nodeOptions, pool);

	const mysqlNodeData = {
		resource,
		operation,
	} as MySqlType;

	try {
		switch (mysqlNodeData.resource) {
			case 'database':
				returnData = await database[mysqlNodeData.operation].execute.call(
					this,
					items,
					runQueries,
					nodeOptions,
				);
				break;
			default:
				throw new NodeOperationError(
					this.getNode(),
					`The operation "${operation}" is not supported!`,
				);
		}
	} finally {
		await pool.end();
	}

	addExecutionHints(this, node, items, operation, node.executeOnce);

	return [returnData];
}
