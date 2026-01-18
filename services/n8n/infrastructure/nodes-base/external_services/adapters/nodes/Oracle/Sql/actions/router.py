"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Oracle/Sql/actions/router.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Oracle/Sql 的路由。导入/依赖:外部:无；内部:n8n-workflow；本地:./database/Database.resource、./node.type、../helpers/interfaces、../helpers/utils 等1项。导出:无。关键函数/方法:router。用于组织该模块路由，绑定控制器与中间件，定义API边界。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Oracle/Sql/actions/router.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Oracle/Sql/actions/router.py

import type { IExecuteFunctions, INodeExecutionData } from 'n8n-workflow';
import { NodeOperationError } from 'n8n-workflow';

import * as database from './database/Database.resource';
import type { OracleDBType } from './node.type';
import { isOracleDBOperation } from './node.type';
import type { OracleDBNodeCredentials, OracleDBNodeOptions } from '../helpers/interfaces';
import { configureQueryRunner } from '../helpers/utils';
import { configureOracleDB } from '../transport';

export async function router(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
	let returnData: INodeExecutionData[] = [];

	const items = this.getInputData();
	const resource = this.getNodeParameter<OracleDBType>('resource', 0);
	const operation = this.getNodeParameter('operation', 0);

	if (!isOracleDBOperation(operation)) {
		throw new NodeOperationError(
			this.getNode(),
			`The operation "${operation}" is not a valid value!`,
		);
	}

	const credentials = await this.getCredentials<OracleDBNodeCredentials>('oracleDBApi');
	const options = this.getNodeParameter('options', 0, {}) as OracleDBNodeOptions;
	const node = this.getNode();
	options.nodeVersion = node.typeVersion;
	options.operation = operation;
	options.autoCommit = options.autoCommit ?? true;

	const pool = await configureOracleDB.call(this, credentials, options);
	const runQueries = configureQueryRunner.call(this, this.getNode(), this.continueOnFail(), pool);
	const oracleDBNodeData: OracleDBType = {
		resource,
		operation,
	};

	switch (oracleDBNodeData.resource) {
		case 'database':
			returnData = await database[oracleDBNodeData.operation].execute.call(
				this,
				runQueries,
				items,
				options,
				pool,
			);
			break;
		default:
			throw new NodeOperationError(
				this.getNode(),
				`The operation "${operation}" is not supported!`,
			);
	}

	if (operation === 'select' && items.length > 1 && !node.executeOnce) {
		this.addExecutionHints({
			message: `This node ran ${items.length} times, once for each input item. To run for the first item only, enable 'execute once' in the node settings`,
			location: 'outputPane',
		});
	}

	return [returnData];
}
