"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtop/actions/common/session.utils.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtop/actions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../../transport、../transport/types。导出:无。关键函数/方法:executeRequestWithSessionManagement、validateAirtopApiResponse。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtop/actions/common/session.utils.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtop/actions/common/session_utils.py

import type { IExecuteFunctions, IDataObject } from 'n8n-workflow';

import {
	validateSessionAndWindowId,
	createSessionAndWindow,
	shouldCreateNewSession,
	validateAirtopApiResponse,
} from '../../GenericFunctions';
import { apiRequest } from '../../transport';
import type { IAirtopResponse } from '../../transport/types';

/**
 * Execute the node operation. Creates and terminates a new session if needed.
 * @param this - The execution context
 * @param index - The index of the node
 * @param request - The request to execute
 * @returns The response from the request
 */
export async function executeRequestWithSessionManagement(
	this: IExecuteFunctions,
	index: number,
	request: {
		method: 'POST' | 'DELETE';
		path: string;
		body: IDataObject;
	},
): Promise<IAirtopResponse> {
	let airtopSessionId = '';
	try {
		const { sessionId, windowId } = shouldCreateNewSession.call(this, index)
			? await createSessionAndWindow.call(this, index)
			: validateSessionAndWindowId.call(this, index);
		airtopSessionId = sessionId;

		const shouldTerminateSession = this.getNodeParameter('autoTerminateSession', index, false);

		const endpoint = request.path.replace('{sessionId}', sessionId).replace('{windowId}', windowId);
		const response = await apiRequest.call(this, request.method, endpoint, request.body);

		validateAirtopApiResponse(this.getNode(), response);

		if (shouldTerminateSession) {
			await apiRequest.call(this, 'DELETE', `/sessions/${sessionId}`);
			this.logger.info(`[${this.getNode().name}] Session terminated.`);
			return response;
		}

		return { sessionId, windowId, ...response };
	} catch (error) {
		// terminate session on error
		if (airtopSessionId) {
			await apiRequest.call(this, 'DELETE', `/sessions/${airtopSessionId}`);
			this.logger.info(`[${this.getNode().name}] Session terminated.`);
		}
		throw error;
	}
}
