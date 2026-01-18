"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/trigger/ChatTrigger/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/trigger/ChatTrigger 的节点。导入/依赖:外部:basic-auth；内部:n8n-workflow；本地:./error、./types。导出:无。关键函数/方法:validateAuth、getCookie。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/trigger/ChatTrigger/GenericFunctions.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/trigger/ChatTrigger/GenericFunctions.py

import basicAuth from 'basic-auth';
import type { ICredentialDataDecryptedObject, IWebhookFunctions } from 'n8n-workflow';

import { ChatTriggerAuthorizationError } from './error';
import type { AuthenticationChatOption } from './types';

export async function validateAuth(context: IWebhookFunctions) {
	const authentication = context.getNodeParameter('authentication') as AuthenticationChatOption;
	const req = context.getRequestObject();
	const headers = context.getHeaderData();

	if (authentication === 'none') {
		return;
	} else if (authentication === 'basicAuth') {
		// Basic authorization is needed to call webhook
		let expectedAuth: ICredentialDataDecryptedObject | undefined;
		try {
			expectedAuth = await context.getCredentials<ICredentialDataDecryptedObject>('httpBasicAuth');
		} catch {}

		if (expectedAuth === undefined || !expectedAuth.user || !expectedAuth.password) {
			// Data is not defined on node so can not authenticate
			throw new ChatTriggerAuthorizationError(500, 'No authentication data defined on node!');
		}

		const providedAuth = basicAuth(req);
		// Authorization data is missing
		if (!providedAuth) throw new ChatTriggerAuthorizationError(401);

		if (providedAuth.name !== expectedAuth.user || providedAuth.pass !== expectedAuth.password) {
			// Provided authentication data is wrong
			throw new ChatTriggerAuthorizationError(403);
		}
	} else if (authentication === 'n8nUserAuth') {
		const webhookName = context.getWebhookName();

		function getCookie(name: string) {
			const value = `; ${headers.cookie}`;
			const parts = value.split(`; ${name}=`);

			if (parts.length === 2) {
				return parts.pop()?.split(';').shift();
			}
			return '';
		}

		const authCookie = getCookie('n8n-auth');
		if (!authCookie && webhookName !== 'setup') {
			// Data is not defined on node so can not authenticate
			throw new ChatTriggerAuthorizationError(500, 'User not authenticated!');
		}
	}

	return;
}
