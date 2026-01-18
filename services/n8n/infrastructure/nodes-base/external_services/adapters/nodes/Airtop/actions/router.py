"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtop/actions/router.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtop/actions 的路由。导入/依赖:外部:无；内部:n8n-workflow；本地:./agent/Agent.resource、./common/output.utils、./extraction/Extraction.resource、./file/File.resource 等5项。导出:无。关键函数/方法:router。用于组织该模块路由，绑定控制器与中间件，定义API边界。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtop/actions/router.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtop/actions/router.py

import type { IExecuteFunctions, INodeExecutionData } from 'n8n-workflow';
import { NodeOperationError } from 'n8n-workflow';

import * as agent from './agent/Agent.resource';
import { cleanOutputForToolUse } from './common/output.utils';
import * as extraction from './extraction/Extraction.resource';
import * as file from './file/File.resource';
import * as interaction from './interaction/Interaction.resource';
import type { AirtopType } from './node.type';
import * as session from './session/Session.resource';
import * as window from './window/Window.resource';
import type { IAirtopNodeExecutionData } from '../transport/types';

export async function router(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
	const operationResult: INodeExecutionData[] = [];
	let responseData: IAirtopNodeExecutionData[] = [];
	const nodeType = this.getNode().type;
	const isCalledAsTool = nodeType.includes('airtopTool');

	const items = this.getInputData();
	const resource = this.getNodeParameter<AirtopType>('resource', 0);
	const operation = this.getNodeParameter('operation', 0);

	const airtopNodeData = {
		resource,
		operation,
	} as AirtopType;

	for (let i = 0; i < items.length; i++) {
		try {
			switch (airtopNodeData.resource) {
				case 'agent':
					responseData = await agent[airtopNodeData.operation].execute.call(this, i);
					break;
				case 'session':
					responseData = await session[airtopNodeData.operation].execute.call(this, i);
					break;
				case 'window':
					responseData = await window[airtopNodeData.operation].execute.call(this, i);
					break;
				case 'interaction':
					responseData = await interaction[airtopNodeData.operation].execute.call(this, i);
					break;
				case 'extraction':
					responseData = await extraction[airtopNodeData.operation].execute.call(this, i);
					break;
				case 'file':
					responseData = await file[airtopNodeData.operation].execute.call(this, i);
					break;
				default:
					throw new NodeOperationError(
						this.getNode(),
						`The resource "${resource}" is not supported!`,
					);
			}

			// Get cleaner output when called as tool
			if (isCalledAsTool) {
				responseData = cleanOutputForToolUse(responseData);
			}

			const executionData = this.helpers.constructExecutionMetaData(responseData, {
				itemData: { item: i },
			});

			operationResult.push(...executionData);
		} catch (error) {
			if (this.continueOnFail()) {
				operationResult.push({
					json: this.getInputData(i)[0].json,
					error: error as NodeOperationError,
				});
			} else {
				throw error;
			}
		}
	}

	return [operationResult];
}
