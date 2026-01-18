"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Analytics/v2/actions/router.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Analytics 的路由。导入/依赖:外部:无；内部:n8n-workflow；本地:./node.type、./report/Report.resource、./userActivity/UserActivity.resource。导出:无。关键函数/方法:router。用于组织该模块路由，绑定控制器与中间件，定义API边界。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Analytics/v2/actions/router.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Analytics/v2/actions/router.py

import type { IExecuteFunctions, INodeExecutionData } from 'n8n-workflow';
import { NodeOperationError } from 'n8n-workflow';

import type { GoogleAnalytics, ReportBasedOnProperty } from './node.type';
import * as report from './report/Report.resource';
import * as userActivity from './userActivity/UserActivity.resource';

export async function router(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
	const items = this.getInputData();
	const returnData: INodeExecutionData[] = [];
	const resource = this.getNodeParameter<GoogleAnalytics>('resource', 0) as string;
	const operation = this.getNodeParameter('operation', 0);

	let responseData;

	const googleAnalytics = {
		resource,
		operation,
	} as GoogleAnalytics;

	for (let i = 0; i < items.length; i++) {
		try {
			switch (googleAnalytics.resource) {
				case 'report':
					const propertyType = this.getNodeParameter('propertyType', 0) as string;
					const operationBasedOnProperty =
						`${googleAnalytics.operation}${propertyType}` as ReportBasedOnProperty;
					responseData = await report[operationBasedOnProperty].execute.call(this, i);
					break;
				case 'userActivity':
					responseData = await userActivity[googleAnalytics.operation].execute.call(this, i);
					break;
				default:
					throw new NodeOperationError(this.getNode(), `The resource "${resource}" is not known`);
			}

			returnData.push(...responseData);
		} catch (error) {
			if (this.continueOnFail()) {
				const executionErrorData = this.helpers.constructExecutionMetaData(
					this.helpers.returnJsonArray({ error: error.message }),
					{ itemData: { item: i } },
				);
				returnData.push(...executionErrorData);
				continue;
			}
			throw error;
		}
	}
	return [returnData];
}
