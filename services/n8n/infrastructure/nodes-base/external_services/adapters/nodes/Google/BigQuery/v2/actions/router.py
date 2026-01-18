"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/BigQuery/v2/actions/router.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/BigQuery 的路由。导入/依赖:外部:无；内部:n8n-workflow；本地:./database/Database.resource、./node.type。导出:无。关键函数/方法:router。用于组织该模块路由，绑定控制器与中间件，定义API边界。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/BigQuery/v2/actions/router.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/BigQuery/v2/actions/router.py

import type { IExecuteFunctions, INodeExecutionData } from 'n8n-workflow';
import { NodeOperationError } from 'n8n-workflow';

import * as record from './database/Database.resource';
import type { GoogleBigQuery } from './node.type';

export async function router(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
	const resource = this.getNodeParameter<GoogleBigQuery>('resource', 0);
	const operation = this.getNodeParameter('operation', 0);

	let returnData: INodeExecutionData[] = [];

	const googleBigQuery = {
		resource,
		operation,
	} as GoogleBigQuery;

	switch (googleBigQuery.resource) {
		case 'database':
			returnData = await record[googleBigQuery.operation].execute.call(this);
			break;
		default:
			throw new NodeOperationError(this.getNode(), `The resource "${resource}" is not known`);
	}

	return [returnData];
}
