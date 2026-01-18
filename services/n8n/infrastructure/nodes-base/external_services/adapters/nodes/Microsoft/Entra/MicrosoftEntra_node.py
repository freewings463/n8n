"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Entra/MicrosoftEntra.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Entra 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./descriptions、./GenericFunctions。导出:MicrosoftEntra。关键函数/方法:getGroupPropertiesGetAll、getUserPropertiesGetAll。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Entra/MicrosoftEntra.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Entra/MicrosoftEntra_node.py

import type {
	ILoadOptionsFunctions,
	INodePropertyOptions,
	INodeType,
	INodeTypeDescription,
} from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import { groupFields, groupOperations, userFields, userOperations } from './descriptions';
import { getGroupProperties, getGroups, getUserProperties, getUsers } from './GenericFunctions';

export class MicrosoftEntra implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Microsoft Entra ID',
		name: 'microsoftEntra',
		icon: {
			light: 'file:microsoftEntra.svg',
			dark: 'file:microsoftEntra.dark.svg',
		},
		group: ['transform'],
		version: 1,
		subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
		description: 'Interact with Microsoft Entra ID API',
		defaults: {
			name: 'Microsoft Entra ID',
		},
		usableAsTool: true,
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'microsoftEntraOAuth2Api',
				required: true,
			},
		],
		requestDefaults: {
			baseURL: 'https://graph.microsoft.com/v1.0',
			headers: {
				'Content-Type': 'application/json',
			},
		},
		properties: [
			{
				displayName: 'Resource',
				name: 'resource',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Group',
						value: 'group',
					},
					{
						name: 'User',
						value: 'user',
					},
				],
				default: 'user',
			},

			...groupOperations,
			...groupFields,
			...userOperations,
			...userFields,
		],
	};

	methods = {
		loadOptions: {
			getGroupProperties,

			async getGroupPropertiesGetAll(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
				// Filter items not supported for list endpoint
				return (await getGroupProperties.call(this)).filter(
					(x) =>
						![
							'allowExternalSenders',
							'autoSubscribeNewMembers',
							'hideFromAddressLists',
							'hideFromOutlookClients',
							'isSubscribedByMail',
							'unseenCount',
						].includes(x.value as string),
				);
			},

			getUserProperties,

			async getUserPropertiesGetAll(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
				// Filter items not supported for list endpoint
				return (await getUserProperties.call(this)).filter(
					(x) =>
						![
							'aboutMe',
							'birthday',
							'hireDate',
							'interests',
							'mySite',
							'pastProjects',
							'preferredName',
							'responsibilities',
							'schools',
							'skills',
							'mailboxSettings',
						].includes(x.value as string),
				);
			},
		},

		listSearch: {
			getGroups,

			getUsers,
		},
	};
}
