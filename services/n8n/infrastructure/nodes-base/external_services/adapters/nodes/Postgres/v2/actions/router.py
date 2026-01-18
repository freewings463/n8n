"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Postgres/v2/actions/router.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Postgres/v2 的路由。导入/依赖:外部:无；内部:n8n-workflow；本地:./database/Database.resource、./node.type、../utils/utilities、../../transport 等2项。导出:无。关键函数/方法:router、addExecutionHints。用于组织该模块路由，绑定控制器与中间件，定义API边界。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Postgres/v2/actions/router.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Postgres/v2/actions/router.py

import type { IExecuteFunctions, INodeExecutionData } from 'n8n-workflow';
import { NodeOperationError } from 'n8n-workflow';

import * as database from './database/Database.resource';
import type { PostgresType } from './node.type';
import { addExecutionHints } from '../../../../utils/utilities';
import { configurePostgres } from '../../transport';
import type { PostgresNodeCredentials, PostgresNodeOptions } from '../helpers/interfaces';
import { configureQueryRunner } from '../helpers/utils';

export async function router(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
	let returnData: INodeExecutionData[] = [];

	const items = this.getInputData();
	const resource = this.getNodeParameter<PostgresType>('resource', 0);
	const operation = this.getNodeParameter('operation', 0);

	const credentials = await this.getCredentials<PostgresNodeCredentials>('postgres');
	const options = this.getNodeParameter('options', 0, {}) as PostgresNodeOptions;
	const node = this.getNode();
	options.nodeVersion = node.typeVersion;
	options.operation = operation;

	const { db, pgp } = await configurePostgres.call(this, credentials, options);

	const runQueries = configureQueryRunner.call(
		this,
		this.getNode(),
		this.continueOnFail(),
		pgp,
		db,
	);

	const postgresNodeData = {
		resource,
		operation,
	} as PostgresType;

	switch (postgresNodeData.resource) {
		case 'database':
			returnData = await database[postgresNodeData.operation].execute.call(
				this,
				runQueries,
				items,
				options,
				db,
				pgp,
			);
			break;
		default:
			throw new NodeOperationError(
				this.getNode(),
				`The operation "${operation}" is not supported!`,
			);
	}

	addExecutionHints(this, node, items, operation, node.executeOnce);

	return [returnData];
}
