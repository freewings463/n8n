"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Aws/Cognito/methods/listSearch.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Aws/Cognito 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../helpers/interfaces、../helpers/utils、../transport。导出:无。关键函数/方法:formatResults、searchGroups、responseData、searchGroupsForUser、groups、searchUsers、userPoolData、searchUserPools。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Aws/Cognito/methods/listSearch.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Aws/Cognito/methods/listSearch.py

import type {
	IDataObject,
	IExecuteSingleFunctions,
	ILoadOptionsFunctions,
	INodeListSearchItems,
	INodeListSearchResult,
} from 'n8n-workflow';
import { NodeOperationError } from 'n8n-workflow';

import type { IGroup, IUser, IUserAttribute, IUserPool } from '../helpers/interfaces';
import { getUserNameFromExistingUsers, getUserPool } from '../helpers/utils';
import { awsApiRequest, awsApiRequestAllItems } from '../transport';

function formatResults(items: IDataObject[], filter?: string): INodeListSearchItems[] {
	return items
		.map(({ id, name }) => ({
			name: String(name).replace(/ /g, ''),
			value: String(id),
		}))
		.filter(({ name }) => !filter || name.toLowerCase().includes(filter.toLowerCase()))
		.sort((a, b) => a.name.toLowerCase().localeCompare(b.name.toLowerCase()));
}

export async function searchGroups(
	this: ILoadOptionsFunctions,
	filter?: string,
	paginationToken?: string,
): Promise<INodeListSearchResult> {
	const userPoolId = this.getNodeParameter('userPool', undefined, {
		extractValue: true,
	}) as string;
	if (!userPoolId) {
		throw new NodeOperationError(this.getNode(), 'User Pool ID is required to search groups');
	}

	const responseData = (await awsApiRequest.call(
		this,
		'POST',
		'ListGroups',
		JSON.stringify({ UserPoolId: userPoolId, Limit: 50, NextToken: paginationToken }),
	)) as IDataObject;

	const groups = responseData.Groups as IDataObject[];

	const groupsMapped = groups.map(({ GroupName }) => ({
		id: GroupName,
		name: GroupName,
	}));

	const formattedResults = formatResults(groupsMapped, filter);

	return { results: formattedResults, paginationToken: responseData.NextToken };
}

export async function searchGroupsForUser(
	this: ILoadOptionsFunctions,
	filter?: string,
): Promise<INodeListSearchResult> {
	const userPoolId = this.getNodeParameter('userPool', undefined, {
		extractValue: true,
	}) as string;
	const inputUser = this.getNodeParameter('user', undefined, {
		extractValue: true,
	}) as string;

	if (!userPoolId || !inputUser) {
		return { results: [] };
	}

	const userPool = await getUserPool.call(this, userPoolId);

	const usernameAttributes = userPool.UsernameAttributes ?? [];
	const isEmailAuth = usernameAttributes.includes('email');
	const isPhoneAuth = usernameAttributes.includes('phone_number');
	const isEmailOrPhone = isEmailAuth || isPhoneAuth;

	const userName = await getUserNameFromExistingUsers.call(
		this,
		inputUser,
		userPoolId,
		isEmailOrPhone,
	);

	if (!userName) {
		return { results: [] };
	}

	const groups = (await awsApiRequestAllItems.call(
		this,
		'POST',
		'AdminListGroupsForUser',
		{
			Username: userName,
			UserPoolId: userPoolId,
		},
		'Groups',
	)) as unknown as IGroup[];

	const resultGroups = groups
		.filter((group) => !filter || group.GroupName.toLowerCase().includes(filter.toLowerCase()))
		.map((group) => ({
			name: group.GroupName,
			value: group.GroupName,
		}))
		.sort((a, b) => a.name.localeCompare(b.name));

	return { results: resultGroups };
}

export async function searchUsers(
	this: IExecuteSingleFunctions | ILoadOptionsFunctions,
	filter?: string,
	paginationToken?: string,
): Promise<INodeListSearchResult> {
	const userPoolId = this.getNodeParameter('userPool', undefined, { extractValue: true }) as string;

	if (!userPoolId) {
		throw new NodeOperationError(this.getNode(), 'User Pool ID is required to search users');
	}

	const userPoolData = (await awsApiRequest.call(
		this,
		'POST',
		'DescribeUserPool',
		JSON.stringify({ UserPoolId: userPoolId }),
	)) as IDataObject;

	const userPool = userPoolData.UserPool as IUserPool;
	const usernameAttributes = userPool.UsernameAttributes;

	const responseData = (await awsApiRequest.call(
		this,
		'POST',
		'ListUsers',
		JSON.stringify({
			UserPoolId: userPoolId,
			Limit: 50,
			NextToken: paginationToken,
		}),
	)) as IDataObject;

	const users = responseData.Users as IUser[];

	if (!users.length) {
		return { results: [] };
	}

	const userResults = users.map((user) => {
		const attributes: IUserAttribute[] = user.Attributes ?? [];
		const username = user.Username;

		const email = attributes.find((attr) => attr.Name === 'email')?.Value ?? '';
		const phoneNumber = attributes.find((attr) => attr.Name === 'phone_number')?.Value ?? '';
		const sub = attributes.find((attr) => attr.Name === 'sub')?.Value ?? '';

		const name = usernameAttributes?.includes('email')
			? email
			: usernameAttributes?.includes('phone_number')
				? phoneNumber
				: username;

		return { id: sub, name, value: sub };
	});

	return { results: formatResults(userResults, filter), paginationToken: responseData.NextToken };
}

export async function searchUserPools(
	this: ILoadOptionsFunctions,
	filter?: string,
	paginationToken?: string,
): Promise<INodeListSearchResult> {
	const responseData = (await awsApiRequest.call(
		this,
		'POST',
		'ListUserPools',
		JSON.stringify({ Limit: 50, NextToken: paginationToken }),
	)) as IDataObject;

	const userPools = responseData.UserPools as IUserPool[];

	const userPoolsMapped = userPools.map((userPool) => ({
		id: userPool.Id,
		name: userPool.Name,
	}));

	const formattedResults = formatResults(userPoolsMapped, filter);

	return { results: formattedResults, paginationToken: responseData.NextToken };
}
