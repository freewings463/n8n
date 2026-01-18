"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Discord/v2/transport/helpers.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Discord/v2 的工具。导入/依赖:外部:无；内部:无；本地:无。导出:getCredentialsType。关键函数/方法:getCredentialsType、requestApi。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Discord/v2/transport/helpers.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Discord/v2/transport/helpers.py

import type {
	IDataObject,
	IExecuteFunctions,
	IExecuteSingleFunctions,
	IHookFunctions,
	ILoadOptionsFunctions,
	IRequestOptions,
} from 'n8n-workflow';

export const getCredentialsType = (authentication: string) => {
	let credentialType = '';
	switch (authentication) {
		case 'botToken':
			credentialType = 'discordBotApi';
			break;
		case 'oAuth2':
			credentialType = 'discordOAuth2Api';
			break;
		case 'webhook':
			credentialType = 'discordWebhookApi';
			break;
		default:
			credentialType = 'discordBotApi';
	}
	return credentialType;
};

export async function requestApi(
	this: IHookFunctions | IExecuteFunctions | IExecuteSingleFunctions | ILoadOptionsFunctions,
	options: IRequestOptions,
	credentialType: string,
	endpoint: string,
) {
	let response;
	if (credentialType === 'discordOAuth2Api' && endpoint !== '/users/@me/guilds') {
		const credentials = await this.getCredentials('discordOAuth2Api');
		(options.headers as IDataObject).Authorization = `Bot ${credentials.botToken}`;
		response = await this.helpers.request({ ...options, resolveWithFullResponse: true });
	} else {
		response = await this.helpers.requestWithAuthentication.call(this, credentialType, {
			...options,
			resolveWithFullResponse: true,
		});
	}
	return response;
}
