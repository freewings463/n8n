"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Discord/v2/methods/loadOptions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Discord/v2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../helpers/utils、../transport。导出:无。关键函数/方法:getRoles、userGuilds、checkAccessToGuild、userRoles。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Discord/v2/methods/loadOptions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Discord/v2/methods/loadOptions.py

import type { IDataObject, ILoadOptionsFunctions, INodePropertyOptions } from 'n8n-workflow';

import { checkAccessToGuild } from '../helpers/utils';
import { discordApiRequest } from '../transport';

export async function getRoles(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
	const guildId = this.getNodeParameter('guildId', undefined, {
		extractValue: true,
	}) as string;

	const isOAuth2 = this.getNodeParameter('authentication', '') === 'oAuth2';

	if (isOAuth2) {
		const userGuilds = (await discordApiRequest.call(
			this,
			'GET',
			'/users/@me/guilds',
		)) as IDataObject[];

		checkAccessToGuild(this.getNode(), guildId, userGuilds);
	}

	let response = await discordApiRequest.call(this, 'GET', `/guilds/${guildId}/roles`);

	const operations = this.getNodeParameter('operation') as string;

	if (operations === 'roleRemove') {
		const userId = this.getNodeParameter('userId', undefined, {
			extractValue: true,
		}) as string;

		const userRoles = ((
			await discordApiRequest.call(this, 'GET', `/guilds/${guildId}/members/${userId}`)
		).roles || []) as string[];

		response = response.filter((role: IDataObject) => {
			return userRoles.includes(role.id as string);
		});
	}

	return response
		.filter((role: IDataObject) => role.name !== '@everyone' && !role.managed)
		.map((role: IDataObject) => ({
			name: role.name as string,
			value: role.id as string,
		}));
}
