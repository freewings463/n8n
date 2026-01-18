"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Discord/v2/methods/listSearch.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Discord/v2 的节点。导入/依赖:外部:无；内部:无；本地:../helpers/utils、../transport。导出:无。关键函数/方法:getGuildId、userGuilds、checkAccessToGuild、checkBotAccessToGuild、guildSearch、response、botId、channelSearch、textChannelSearch、categorySearch 等1项。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Discord/v2/methods/listSearch.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Discord/v2/methods/listSearch.py

import {
	type IDataObject,
	type ILoadOptionsFunctions,
	type INodeListSearchResult,
} from 'n8n-workflow';

import { checkAccessToGuild } from '../helpers/utils';
import { discordApiRequest } from '../transport';

async function getGuildId(this: ILoadOptionsFunctions) {
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

	return guildId;
}

async function checkBotAccessToGuild(this: ILoadOptionsFunctions, guildId: string, botId: string) {
	try {
		const members: Array<{ user: { id: string } }> = await discordApiRequest.call(
			this,
			'GET',
			`/guilds/${guildId}/members`,
			undefined,
			{ limit: 1000 },
		);

		return members.some((member) => member.user.id === botId);
	} catch (error) {}

	return false;
}

export async function guildSearch(this: ILoadOptionsFunctions): Promise<INodeListSearchResult> {
	const response = (await discordApiRequest.call(
		this,
		'GET',
		'/users/@me/guilds',
	)) as IDataObject[];

	let guilds: IDataObject[] = [];

	const isOAuth2 = this.getNodeParameter('authentication', 0) === 'oAuth2';

	if (isOAuth2) {
		const botId = (await discordApiRequest.call(this, 'GET', '/users/@me')).id as string;

		for (const guild of response) {
			if (!(await checkBotAccessToGuild.call(this, guild.id as string, botId))) continue;
			guilds.push(guild);
		}
	} else {
		guilds = response;
	}

	return {
		results: guilds.map((guild) => ({
			name: guild.name as string,
			value: guild.id as string,
			url: `https://discord.com/channels/${guild.id}`,
		})),
	};
}

export async function channelSearch(this: ILoadOptionsFunctions): Promise<INodeListSearchResult> {
	const guildId = await getGuildId.call(this);
	const response = await discordApiRequest.call(this, 'GET', `/guilds/${guildId}/channels`);

	return {
		results: (response as IDataObject[])
			.filter((cannel) => cannel.type !== 4) // Filter out categories
			.map((channel) => ({
				name: channel.name as string,
				value: channel.id as string,
				url: `https://discord.com/channels/${guildId}/${channel.id}`,
			})),
	};
}

export async function textChannelSearch(
	this: ILoadOptionsFunctions,
): Promise<INodeListSearchResult> {
	const guildId = await getGuildId.call(this);

	const response = await discordApiRequest.call(this, 'GET', `/guilds/${guildId}/channels`);

	return {
		results: (response as IDataObject[])
			.filter((cannel) => ![2, 4].includes(cannel.type as number)) // Only text channels
			.map((channel) => ({
				name: channel.name as string,
				value: channel.id as string,
				url: `https://discord.com/channels/${guildId}/${channel.id}`,
			})),
	};
}

export async function categorySearch(this: ILoadOptionsFunctions): Promise<INodeListSearchResult> {
	const guildId = await getGuildId.call(this);

	const response = await discordApiRequest.call(this, 'GET', `/guilds/${guildId}/channels`);

	return {
		results: (response as IDataObject[])
			.filter((cannel) => cannel.type === 4) // Return only categories
			.map((channel) => ({
				name: channel.name as string,
				value: channel.id as string,
				url: `https://discord.com/channels/${guildId}/${channel.id}`,
			})),
	};
}

export async function userSearch(
	this: ILoadOptionsFunctions,
	_filter?: string,
	paginationToken?: string,
): Promise<INodeListSearchResult> {
	const guildId = await getGuildId.call(this);

	const limit = 100;
	const qs = { limit, after: paginationToken };

	const response = await discordApiRequest.call(
		this,
		'GET',
		`/guilds/${guildId}/members`,
		undefined,
		qs,
	);

	if (response.length === 0) {
		return {
			results: [],
			paginationToken: undefined,
		};
	}

	let lastUserId;

	//less then limit means that there are no more users to return, so leave lastUserId undefined
	if (!(response.length < limit)) {
		lastUserId = response[response.length - 1].user.id as string;
	}

	return {
		results: (response as Array<{ user: IDataObject }>).map(({ user }) => ({
			name: user.username as string,
			value: user.id as string,
		})),
		paginationToken: lastUserId,
	};
}
