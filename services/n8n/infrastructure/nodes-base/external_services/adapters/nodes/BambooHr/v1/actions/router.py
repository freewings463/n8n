"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/BambooHr/v1/actions/router.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/BambooHr/v1 的路由。导入/依赖:外部:无；内部:n8n-workflow；本地:./companyReport、./employee、./employeeDocument、./file 等1项。导出:无。关键函数/方法:router。用于组织该模块路由，绑定控制器与中间件，定义API边界。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/BambooHr/v1/actions/router.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/BambooHr/v1/actions/router.py

import type { IExecuteFunctions, INodeExecutionData } from 'n8n-workflow';

import * as companyReport from './companyReport';
import * as employee from './employee';
import * as employeeDocument from './employeeDocument';
import * as file from './file';
import type { BambooHr } from './Interfaces';

export async function router(this: IExecuteFunctions): Promise<INodeExecutionData[]> {
	const items = this.getInputData();
	const operationResult: INodeExecutionData[] = [];

	for (let i = 0; i < items.length; i++) {
		const resource = this.getNodeParameter<BambooHr>('resource', i);
		const operation = this.getNodeParameter('operation', i);

		const bamboohr = {
			resource,
			operation,
		} as BambooHr;

		if (bamboohr.operation === 'delete') {
			//@ts-ignore
			bamboohr.operation = 'del';
		}

		try {
			if (bamboohr.resource === 'employee') {
				operationResult.push(...(await employee[bamboohr.operation].execute.call(this, i)));
			} else if (bamboohr.resource === 'employeeDocument') {
				//@ts-ignore
				operationResult.push(...(await employeeDocument[bamboohr.operation].execute.call(this, i)));
			} else if (bamboohr.resource === 'file') {
				//@ts-ignore
				operationResult.push(...(await file[bamboohr.operation].execute.call(this, i)));
			} else if (bamboohr.resource === 'companyReport') {
				//@ts-ignore
				operationResult.push(...(await companyReport[bamboohr.operation].execute.call(this, i)));
			}
		} catch (err) {
			if (this.continueOnFail()) {
				operationResult.push({ json: this.getInputData(i)[0].json, error: err });
			} else {
				throw err;
			}
		}
	}

	return operationResult;
}
