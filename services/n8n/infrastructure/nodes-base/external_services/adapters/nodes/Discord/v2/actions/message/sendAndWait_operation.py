"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Discord/v2/actions/message/sendAndWait.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Discord/v2 的节点。导入/依赖:外部:无；内部:无；本地:../sendAndWait/utils、../common.description。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Discord/v2/actions/message/sendAndWait.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Discord/v2/actions/message/sendAndWait_operation.py

import type {
	IDataObject,
	IExecuteFunctions,
	INodeExecutionData,
	INodeProperties,
} from 'n8n-workflow';

import { getSendAndWaitProperties } from '../../../../../utils/sendAndWait/utils';
import {
	createSendAndWaitMessageBody,
	parseDiscordError,
	prepareErrorData,
	sendDiscordMessage,
} from '../../helpers/utils';
import { sendToProperties } from '../common.description';

export const description: INodeProperties[] = getSendAndWaitProperties(
	sendToProperties,
	'message',
	undefined,
	{
		noButtonStyle: true,
		defaultApproveLabel: '✓ Approve',
		defaultDisapproveLabel: '✗ Decline',
	},
).filter((p) => p.name !== 'subject');

export async function execute(
	this: IExecuteFunctions,
	guildId: string,
	userGuilds: IDataObject[],
): Promise<INodeExecutionData[]> {
	const items = this.getInputData();

	const isOAuth2 = this.getNodeParameter('authentication', 0) === 'oAuth2';

	try {
		await sendDiscordMessage.call(this, {
			guildId,
			userGuilds,
			isOAuth2,
			body: createSendAndWaitMessageBody(this),
		});
	} catch (error) {
		const err = parseDiscordError.call(this, error, 0);

		if (this.continueOnFail()) {
			return prepareErrorData.call(this, err, 0);
		}

		throw err;
	}

	return items;
}
