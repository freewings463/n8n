"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/Guardrails/actions/execute.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/Guardrails/actions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./process、./types、../helpers/configureNodeInputs、../helpers/model。导出:无。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/Guardrails/actions/execute.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/Guardrails/actions/execute.py

import type { IExecuteFunctions, INodeExecutionData } from 'n8n-workflow';

import { process } from './process';
import type { GuardrailsOptions } from './types';
import { hasLLMGuardrails } from '../helpers/configureNodeInputs';
import { getChatModel } from '../helpers/model';

export async function execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
	const items = this.getInputData();
	const operation = this.getNodeParameter('operation', 0) as 'classify' | 'sanitize';
	const model = hasLLMGuardrails(this.getNodeParameter('guardrails', 0) as GuardrailsOptions)
		? await getChatModel.call(this)
		: null;

	const failedItems: INodeExecutionData[] = [];
	const passedItems: INodeExecutionData[] = [];
	for (let i = 0; i < items.length; i++) {
		try {
			const responseData = await process.call(this, i, model);
			if (responseData.passed) {
				passedItems.push({
					json: { guardrailsInput: responseData.guardrailsInput, ...responseData.passed },
					pairedItem: { item: i },
				});
			}
			if (responseData.failed) {
				failedItems.push({
					json: { guardrailsInput: responseData.guardrailsInput, ...responseData.failed },
					pairedItem: { item: i },
				});
			}
		} catch (error) {
			if (this.continueOnFail()) {
				failedItems.push({
					json: { error: error.message, guardrailsInput: '' },
					pairedItem: { item: i },
				});
			} else {
				throw error;
			}
		}
	}

	if (operation === 'classify') {
		return [passedItems, failedItems];
	}

	return [passedItems];
}
