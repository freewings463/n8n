"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Splunk/v2/actions/user/create.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Splunk/v2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../utils/utilities、../helpers/interfaces、../helpers/utils、../../transport。导出:description。关键函数/方法:execute、populate、responseData。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Splunk/v2/actions/user/create.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Splunk/v2/actions/user/create_operation.py

import type { INodeProperties, IExecuteFunctions, IDataObject } from 'n8n-workflow';

import { updateDisplayOptions } from '../../../../../utils/utilities';
import type { SplunkFeedResponse } from '../../helpers/interfaces';
import { formatFeed, populate } from '../../helpers/utils';
import { splunkApiRequest } from '../../transport';

const properties: INodeProperties[] = [
	{
		displayName: 'Name',
		name: 'name',
		description: 'Login name of the user',
		type: 'string',
		required: true,
		default: '',
	},
	{
		// eslint-disable-next-line n8n-nodes-base/node-param-display-name-wrong-for-dynamic-multi-options
		displayName: 'Roles',
		name: 'roles',
		type: 'multiOptions',
		description:
			'Comma-separated list of roles to assign to the user. Choose from the list, or specify IDs using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
		required: true,
		default: ['user'],
		typeOptions: {
			loadOptionsMethod: 'getRoles',
		},
	},
	{
		displayName: 'Password',
		name: 'password',
		type: 'string',
		typeOptions: { password: true },
		required: true,
		default: '',
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		options: [
			{
				displayName: 'Email',
				name: 'email',
				type: 'string',
				placeholder: 'name@email.com',
				default: '',
			},
			{
				displayName: 'Full Name',
				name: 'realname',
				type: 'string',
				default: '',
				description: 'Full name of the user',
			},
		],
	},
];

const displayOptions = {
	show: {
		resource: ['user'],
		operation: ['create'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(
	this: IExecuteFunctions,
	i: number,
): Promise<IDataObject | IDataObject[]> {
	// https://docs.splunk.com/Documentation/Splunk/8.2.2/RESTREF/RESTaccess#authentication.2Fusers

	const roles = this.getNodeParameter('roles', i) as string[];

	const body = {
		name: this.getNodeParameter('name', i),
		roles,
		password: this.getNodeParameter('password', i),
	} as IDataObject;

	const additionalFields = this.getNodeParameter('additionalFields', i);

	populate(additionalFields, body);

	const endpoint = '/services/authentication/users';
	const responseData = (await splunkApiRequest.call(
		this,
		'POST',
		endpoint,
		body,
	)) as SplunkFeedResponse;
	const returnData = formatFeed(responseData);

	return returnData;
}
