"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Mattermost/v1/actions/channel/members/execute.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Mattermost/v1 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../../transport。导出:无。关键函数/方法:members。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Mattermost/v1/actions/channel/members/execute.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Mattermost/v1/actions/channel/members/execute.py

import type { IExecuteFunctions, IDataObject, INodeExecutionData } from 'n8n-workflow';

import { apiRequest, apiRequestAllItems } from '../../../transport';

export async function members(
	this: IExecuteFunctions,
	index: number,
): Promise<INodeExecutionData[]> {
	const channelId = this.getNodeParameter('channelId', index) as string;
	const returnAll = this.getNodeParameter('returnAll', index);
	const resolveData = this.getNodeParameter('resolveData', index);
	const limit = this.getNodeParameter('limit', index, 0);

	const body = {} as IDataObject;
	const qs = {} as IDataObject;
	const requestMethod = 'GET';
	const endpoint = `channels/${channelId}/members`;

	if (!returnAll) {
		qs.per_page = this.getNodeParameter('limit', index);
	}

	let responseData;

	if (returnAll) {
		responseData = await apiRequestAllItems.call(this, requestMethod, endpoint, body, qs);
	} else {
		responseData = await apiRequest.call(this, requestMethod, endpoint, body, qs);
		if (limit) {
			responseData = responseData.slice(0, limit);
		}
		if (resolveData) {
			const userIds: string[] = [];
			for (const data of responseData) {
				userIds.push(data.user_id as string);
			}
			if (userIds.length > 0) {
				responseData = await apiRequest.call(this, 'POST', 'users/ids', userIds, qs);
			}
		}
	}

	return this.helpers.returnJsonArray(responseData as IDataObject[]);
}
