"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/TheHiveProject/actions/router.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/TheHiveProject/actions 的路由。导入/依赖:外部:无；内部:n8n-workflow；本地:./alert、./case、./comment、./log 等5项。导出:无。关键函数/方法:router。用于组织该模块路由，绑定控制器与中间件，定义API边界。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/TheHiveProject/actions/router.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/TheHiveProject/actions/router.py

import type { IExecuteFunctions, INodeExecutionData } from 'n8n-workflow';
import { NodeOperationError } from 'n8n-workflow';

import * as alert from './alert';
import * as case_ from './case';
import * as comment from './comment';
import * as log from './log';
import type { TheHiveType } from './node.type';
import * as observable from './observable';
import * as page from './page';
import * as query from './query';
import * as task from './task';

export async function router(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
	const items = this.getInputData();
	const returnData: INodeExecutionData[] = [];
	const length = items.length;

	const resource = this.getNodeParameter<TheHiveType>('resource', 0);
	const operation = this.getNodeParameter('operation', 0);

	let executionData: INodeExecutionData[] = [];

	const theHiveNodeData = {
		resource,
		operation,
	} as TheHiveType;

	for (let i = 0; i < length; i++) {
		try {
			switch (theHiveNodeData.resource) {
				case 'alert':
					executionData = await alert[theHiveNodeData.operation].execute.call(this, i, items[i]);
					break;
				case 'case':
					executionData = await case_[theHiveNodeData.operation].execute.call(this, i, items[i]);
					break;
				case 'comment':
					executionData = await comment[theHiveNodeData.operation].execute.call(this, i);
					break;
				case 'log':
					executionData = await log[theHiveNodeData.operation].execute.call(this, i, items[i]);
					break;
				case 'observable':
					executionData = await observable[theHiveNodeData.operation].execute.call(
						this,
						i,
						items[i],
					);
					break;
				case 'page':
					executionData = await page[theHiveNodeData.operation].execute.call(this, i);
					break;
				case 'query':
					executionData = await query[theHiveNodeData.operation].execute.call(this, i);
					break;
				case 'task':
					executionData = await task[theHiveNodeData.operation].execute.call(this, i, items[i]);
					break;
				default:
					throw new NodeOperationError(
						this.getNode(),
						`The operation "${operation}" is not supported!`,
					);
			}
			returnData.push(...executionData);
		} catch (error) {
			if (this.continueOnFail()) {
				executionData = this.helpers.constructExecutionMetaData(
					this.helpers.returnJsonArray({ error: error.message }),
					{ itemData: { item: i } },
				);
				returnData.push(...executionData);
				continue;
			}
			throw error;
		}
	}
	return [returnData];
}
