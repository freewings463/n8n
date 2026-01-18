"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Teams/v2/actions/router.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Teams 的路由。导入/依赖:外部:无；内部:无；本地:./channel、./channelMessage、./chatMessage、./node.type 等2项。导出:无。关键函数/方法:router。用于组织该模块路由，绑定控制器与中间件，定义API边界。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Teams/v2/actions/router.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Teams/v2/actions/router.py

import {
	type IExecuteFunctions,
	type IDataObject,
	type INodeExecutionData,
	NodeOperationError,
	SEND_AND_WAIT_OPERATION,
} from 'n8n-workflow';

import * as channel from './channel';
import * as channelMessage from './channelMessage';
import * as chatMessage from './chatMessage';
import type { MicrosoftTeamsType } from './node.type';
import * as task from './task';
import { configureWaitTillDate } from '../../../../../utils/sendAndWait/configureWaitTillDate.util';

export async function router(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
	const items = this.getInputData();
	const returnData: INodeExecutionData[] = [];
	let responseData;

	const resource = this.getNodeParameter<MicrosoftTeamsType>('resource', 0);
	const operation = this.getNodeParameter('operation', 0);

	const nodeVersion = this.getNode().typeVersion;
	const instanceId = this.getInstanceId();

	const microsoftTeamsTypeData = {
		resource,
		operation,
	} as MicrosoftTeamsType;

	if (
		microsoftTeamsTypeData.resource === 'chatMessage' &&
		microsoftTeamsTypeData.operation === SEND_AND_WAIT_OPERATION
	) {
		await chatMessage[microsoftTeamsTypeData.operation].execute.call(this, 0, instanceId);

		const waitTill = configureWaitTillDate(this);

		await this.putExecutionToWait(waitTill);
		return [items];
	}

	for (let i = 0; i < items.length; i++) {
		try {
			switch (microsoftTeamsTypeData.resource) {
				case 'channel':
					responseData = await channel[microsoftTeamsTypeData.operation].execute.call(this, i);
					break;
				case 'channelMessage':
					responseData = await channelMessage[microsoftTeamsTypeData.operation].execute.call(
						this,
						i,
						nodeVersion,
						instanceId,
					);
					break;
				case 'chatMessage':
					responseData = await chatMessage[microsoftTeamsTypeData.operation].execute.call(
						this,
						i,
						instanceId,
					);
					break;
				case 'task':
					responseData = await task[microsoftTeamsTypeData.operation].execute.call(this, i);
					break;
				default:
					throw new NodeOperationError(
						this.getNode(),
						`The operation "${operation}" is not supported!`,
					);
			}

			const executionData = this.helpers.constructExecutionMetaData(
				this.helpers.returnJsonArray(responseData as IDataObject),
				{ itemData: { item: i } },
			);

			returnData.push(...executionData);
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
