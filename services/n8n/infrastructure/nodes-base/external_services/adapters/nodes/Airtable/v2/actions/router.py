"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtable/v2/actions/router.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtable/v2 的路由。导入/依赖:外部:无；内部:n8n-workflow；本地:./base/Base.resource、./node.type、./record/Record.resource。导出:无。关键函数/方法:router。用于组织该模块路由，绑定控制器与中间件，定义API边界。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtable/v2/actions/router.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtable/v2/actions/router.py

import type { IExecuteFunctions, INodeExecutionData } from 'n8n-workflow';
import { NodeOperationError } from 'n8n-workflow';

import * as base from './base/Base.resource';
import type { AirtableType } from './node.type';
import * as record from './record/Record.resource';

export async function router(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
	let returnData: INodeExecutionData[] = [];

	const items = this.getInputData();
	const resource = this.getNodeParameter<AirtableType>('resource', 0);
	const operation = this.getNodeParameter('operation', 0);

	const airtableNodeData = {
		resource,
		operation,
	} as AirtableType;

	try {
		switch (airtableNodeData.resource) {
			case 'record':
				const baseId = this.getNodeParameter('base', 0, undefined, {
					extractValue: true,
				}) as string;

				const table = encodeURI(
					this.getNodeParameter('table', 0, undefined, {
						extractValue: true,
					}) as string,
				);
				returnData = await record[airtableNodeData.operation].execute.call(
					this,
					items,
					baseId,
					table,
				);
				break;
			case 'base':
				returnData = await base[airtableNodeData.operation].execute.call(this, items);
				break;
			default:
				throw new NodeOperationError(
					this.getNode(),
					`The operation "${operation}" is not supported!`,
				);
		}
	} catch (error) {
		if (
			error.description &&
			(error.description as string).includes('cannot accept the provided value')
		) {
			error.description = `${error.description}. Consider using 'Typecast' option`;
		}
		throw error;
	}

	return [returnData];
}
