"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Teams/v2/actions/channel/deleteChannel.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Teams 的节点。导入/依赖:外部:@utils/utilities；内部:n8n-workflow；本地:../../descriptions、../../transport。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Teams/v2/actions/channel/deleteChannel.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Teams/v2/actions/channel/deleteChannel_operation.py

import { type INodeProperties, type IExecuteFunctions, NodeOperationError } from 'n8n-workflow';

import { updateDisplayOptions } from '@utils/utilities';

import { channelRLC, teamRLC } from '../../descriptions';
import { microsoftApiRequest } from '../../transport';

const properties: INodeProperties[] = [teamRLC, channelRLC];

const displayOptions = {
	show: {
		resource: ['channel'],
		operation: ['deleteChannel'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, i: number) {
	//https://docs.microsoft.com/en-us/graph/api/channel-delete?view=graph-rest-beta&tabs=http

	try {
		const teamId = this.getNodeParameter('teamId', i, '', { extractValue: true }) as string;
		const channelId = this.getNodeParameter('channelId', i, '', { extractValue: true }) as string;

		await microsoftApiRequest.call(this, 'DELETE', `/v1.0/teams/${teamId}/channels/${channelId}`);
		return { success: true };
	} catch (error) {
		throw new NodeOperationError(
			this.getNode(),
			"The channel you are trying to delete doesn't exist",
			{
				description: "Check that the 'Channel' parameter is correctly set",
			},
		);
	}
}
