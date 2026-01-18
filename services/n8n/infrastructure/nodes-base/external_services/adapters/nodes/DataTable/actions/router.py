"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/DataTable/actions/router.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/DataTable/actions 的路由。导入/依赖:外部:无；内部:n8n-workflow；本地:./row/Row.resource、./table/Table.resource、../common/fields、../common/utils。导出:无。关键函数/方法:hasBulkExecute、hasComplexId、router。用于组织该模块路由，绑定控制器与中间件，定义API边界。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/DataTable/actions/router.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/DataTable/actions/router.py

import type { IExecuteFunctions, INodeExecutionData, AllEntities } from 'n8n-workflow';
import { NodeApiError, NodeOperationError } from 'n8n-workflow';

import * as row from './row/Row.resource';
import * as table from './table/Table.resource';
import { DATA_TABLE_ID_FIELD } from '../common/fields';
import { getDataTableProxyExecute } from '../common/utils';

type DataTableNodeType = AllEntities<{
	row: 'insert' | 'get' | 'rowExists' | 'rowNotExists' | 'deleteRows' | 'update' | 'upsert';
	table: 'create' | 'delete' | 'list' | 'update';
}>;

const BULK_OPERATIONS = ['insert'] as const;

function hasBulkExecute(operation: string): operation is (typeof BULK_OPERATIONS)[number] {
	return (BULK_OPERATIONS as readonly string[]).includes(operation);
}

function hasComplexId(ctx: IExecuteFunctions) {
	const dataTableIdExpr = ctx.getNodeParameter(`${DATA_TABLE_ID_FIELD}.value`, 0, undefined, {
		rawExpressions: true,
	});

	return typeof dataTableIdExpr === 'string' && dataTableIdExpr.includes('{');
}

export async function router(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
	let operationResult: INodeExecutionData[] = [];
	let responseData: INodeExecutionData[] = [];

	const items = this.getInputData();
	const resource = this.getNodeParameter('resource', 0);
	const operation = this.getNodeParameter('operation', 0);

	const dataTableNodeData = {
		resource,
		operation,
	} as DataTableNodeType;

	if (dataTableNodeData.resource === 'table') {
		// Table operations
		for (let i = 0; i < items.length; i++) {
			try {
				const tableOperation =
					dataTableNodeData.operation === 'delete'
						? table.deleteTable
						: table[dataTableNodeData.operation];
				responseData = await tableOperation.execute.call(this, i);
				const executionData = this.helpers.constructExecutionMetaData(responseData, {
					itemData: { item: i },
				});
				operationResult = operationResult.concat(executionData);
			} catch (error) {
				if (this.continueOnFail()) {
					const inputData = this.getInputData(i)[0].json;
					if (error instanceof NodeApiError || error instanceof NodeOperationError) {
						operationResult.push({ json: inputData, error });
					} else {
						operationResult.push({
							json: inputData,
							error: new NodeOperationError(this.getNode(), error as Error),
						});
					}
				} else {
					throw error;
				}
			}
		}
	} else if (hasBulkExecute(dataTableNodeData.operation) && !hasComplexId(this)) {
		// Row bulk operations
		try {
			const proxy = await getDataTableProxyExecute(this);

			responseData = await row[dataTableNodeData.operation]['executeBulk'].call(this, proxy);

			operationResult = responseData;
		} catch (error) {
			if (this.continueOnFail()) {
				if (error instanceof NodeApiError || error instanceof NodeOperationError) {
					operationResult = this.getInputData().map((json) => ({ json, error }));
				} else {
					operationResult = this.getInputData().map((json) => ({ json }));
				}
			} else {
				throw error;
			}
		}
	} else {
		// Row operations
		for (let i = 0; i < items.length; i++) {
			try {
				responseData = await row[dataTableNodeData.operation].execute.call(this, i);
				const executionData = this.helpers.constructExecutionMetaData(responseData, {
					itemData: { item: i },
				});

				// pushing here risks stack overflows for very high numbers (~100k) of results on filter-based queries (update, get, etc.)
				operationResult = operationResult.concat(executionData);
			} catch (error) {
				if (this.continueOnFail()) {
					const inputData = this.getInputData(i)[0].json;
					if (error instanceof NodeApiError || error instanceof NodeOperationError) {
						operationResult.push({ json: inputData, error });
					} else {
						operationResult.push({ json: inputData });
					}
				} else {
					throw error;
				}
			}
		}
	}

	return [operationResult];
}
