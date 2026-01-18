"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Mattermost/v1/actions/user/getAll/execute.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Mattermost/v1 的节点。导入/依赖:外部:change-case；内部:n8n-workflow；本地:../../transport。导出:无。关键函数/方法:getAll。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Mattermost/v1/actions/user/getAll/execute.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Mattermost/v1/actions/user/getAll/execute.py

import { snakeCase } from 'change-case';
import type { IExecuteFunctions, IDataObject, INodeExecutionData } from 'n8n-workflow';
import { NodeOperationError } from 'n8n-workflow';

import { apiRequest, apiRequestAllItems } from '../../../transport';

export async function getAll(
	this: IExecuteFunctions,
	index: number,
): Promise<INodeExecutionData[]> {
	const returnAll = this.getNodeParameter('returnAll', index);
	const additionalFields = this.getNodeParameter('additionalFields', index);

	const qs = {} as IDataObject;
	const requestMethod = 'GET';
	const endpoint = '/users';
	const body = {} as IDataObject;

	if (additionalFields.inTeam) {
		qs.in_team = additionalFields.inTeam;
	}

	if (additionalFields.notInTeam) {
		qs.not_in_team = additionalFields.notInTeam;
	}

	if (additionalFields.inChannel) {
		qs.in_channel = additionalFields.inChannel;
	}

	if (additionalFields.notInChannel) {
		qs.not_in_channel = additionalFields.notInChannel;
	}

	if (additionalFields.sort) {
		qs.sort = snakeCase(additionalFields.sort as string);
	}

	const validRules = {
		inTeam: ['last_activity_at', 'created_at', 'username'],
		inChannel: ['status', 'username'],
	};

	if (additionalFields.sort) {
		if (additionalFields.inTeam !== undefined || additionalFields.inChannel !== undefined) {
			if (
				additionalFields.inTeam !== undefined &&
				!validRules.inTeam.includes(snakeCase(additionalFields.sort as string))
			) {
				throw new NodeOperationError(
					this.getNode(),
					`When In Team is set the only valid values for sorting are ${validRules.inTeam.join(
						',',
					)}`,
					{ itemIndex: index },
				);
			}
			if (
				additionalFields.inChannel !== undefined &&
				!validRules.inChannel.includes(snakeCase(additionalFields.sort as string))
			) {
				throw new NodeOperationError(
					this.getNode(),
					`When In Channel is set the only valid values for sorting are ${validRules.inChannel.join(
						',',
					)}`,
					{ itemIndex: index },
				);
			}
			if (additionalFields.inChannel === '' && additionalFields.sort !== 'username') {
				throw new NodeOperationError(
					this.getNode(),
					'When sort is different than username In Channel must be set',
					{ itemIndex: index },
				);
			}

			if (additionalFields.inTeam === '' && additionalFields.sort !== 'username') {
				throw new NodeOperationError(
					this.getNode(),
					'When sort is different than username In Team must be set',
					{ itemIndex: index },
				);
			}
		} else {
			throw new NodeOperationError(
				this.getNode(),
				"When sort is defined either 'in team' or 'in channel' must be defined",
				{ itemIndex: index },
			);
		}
	}

	if (additionalFields.sort === 'username') {
		qs.sort = '';
	}

	if (!returnAll) {
		qs.per_page = this.getNodeParameter('limit', index);
	}

	let responseData;

	if (returnAll) {
		responseData = await apiRequestAllItems.call(this, requestMethod, endpoint, body, qs);
	} else {
		responseData = await apiRequest.call(this, requestMethod, endpoint, body, qs);
	}

	return this.helpers.returnJsonArray(responseData as IDataObject[]);
}
