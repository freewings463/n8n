"""
MIGRATION-META:
  source_path: packages/nodes-base/utils/sendAndWait/configureWaitTillDate.util.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/utils/sendAndWait 的工具。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:configureWaitTillDate。关键函数/方法:configureWaitTillDate。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Integration package defaulted to infrastructure/external_services
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/utils/sendAndWait/configureWaitTillDate.util.ts -> services/n8n/infrastructure/nodes-base/external_services/utils/sendAndWait/configureWaitTillDate_util.py

import { ApplicationError, NodeOperationError, WAIT_INDEFINITELY } from 'n8n-workflow';
import type { IExecuteFunctions, IDataObject } from 'n8n-workflow';

export function configureWaitTillDate(
	context: IExecuteFunctions,
	location: 'options' | 'root' = 'options',
) {
	let waitTill = WAIT_INDEFINITELY;
	let limitOptions: IDataObject = {};

	if (location === 'options') {
		limitOptions = context.getNodeParameter('options.limitWaitTime.values', 0, {}) as {
			limitType?: string;
			resumeAmount?: number;
			resumeUnit?: string;
			maxDateAndTime?: string;
		};
	} else {
		const limitWaitTime = context.getNodeParameter('limitWaitTime', 0, false);
		if (limitWaitTime) {
			limitOptions.limitType = context.getNodeParameter('limitType', 0, 'afterTimeInterval');

			if (limitOptions.limitType === 'afterTimeInterval') {
				limitOptions.resumeAmount = context.getNodeParameter('resumeAmount', 0, 1) as number;
				limitOptions.resumeUnit = context.getNodeParameter('resumeUnit', 0, 'hours');
			} else {
				limitOptions.maxDateAndTime = context.getNodeParameter('maxDateAndTime', 0, '');
			}
		}
	}

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
				throw new ApplicationError('Invalid date format');
			}
		} catch (error) {
			throw new NodeOperationError(context.getNode(), 'Could not configure Limit Wait Time', {
				description: error.message,
			});
		}
	}

	return waitTill;
}
