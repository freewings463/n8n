"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/trigger/ChatTrigger/util.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/trigger/ChatTrigger 的工具。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:configureWaitTillDate、configureInputs。关键函数/方法:configureWaitTillDate、configureInputs。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/trigger/ChatTrigger/util.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/trigger/ChatTrigger/util.py

import { NodeOperationError, UserError, WAIT_INDEFINITELY } from 'n8n-workflow';
import type { IExecuteFunctions } from 'n8n-workflow';

export function configureWaitTillDate(context: IExecuteFunctions) {
	let waitTill = WAIT_INDEFINITELY;

	const limitOptions = context.getNodeParameter('options.limitWaitTime.values', 0, {}) as {
		limitType?: string;
		resumeAmount?: number;
		resumeUnit?: string;
		maxDateAndTime?: string;
	};

	if (Object.keys(limitOptions).length) {
		try {
			if (limitOptions.limitType === 'afterTimeInterval') {
				let waitAmount = limitOptions.resumeAmount as number;

				if (limitOptions.resumeUnit === 'minutes') {
					waitAmount *= 60;
				}
				if (limitOptions.resumeUnit === 'hours') {
					waitAmount *= 60 * 60;
				}
				if (limitOptions.resumeUnit === 'days') {
					waitAmount *= 60 * 60 * 24;
				}

				waitAmount *= 1000;
				waitTill = new Date(new Date().getTime() + waitAmount);
			} else {
				waitTill = new Date(limitOptions.maxDateAndTime as string);
			}

			if (isNaN(waitTill.getTime())) {
				throw new UserError('Invalid date format');
			}
		} catch (error) {
			throw new NodeOperationError(context.getNode(), 'Could not configure Limit Wait Time', {
				description: error.message,
			});
		}
	}

	return waitTill;
}

export const configureInputs = (parameters: { options?: { memoryConnection?: boolean } }) => {
	const inputs = [
		{
			type: 'main',
			displayName: 'User Response',
		},
	];
	if (parameters.options?.memoryConnection) {
		return [
			...inputs,
			{
				type: 'ai_memory',
				displayName: 'Memory',
				maxConnections: 1,
			},
		];
	}

	return inputs;
};
