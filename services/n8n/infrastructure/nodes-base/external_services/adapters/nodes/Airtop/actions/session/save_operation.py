"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtop/actions/session/save.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtop/actions 的节点。导入/依赖:外部:无；内部:无；本地:../../transport、../common/fields。导出:description。关键函数/方法:execute、validateAirtopApiResponse。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtop/actions/session/save.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtop/actions/session/save_operation.py

import {
	type IDataObject,
	type IExecuteFunctions,
	type INodeExecutionData,
	type INodeProperties,
} from 'n8n-workflow';

import {
	validateAirtopApiResponse,
	validateProfileName,
	validateRequiredStringField,
	validateSessionId,
} from '../../GenericFunctions';
import { apiRequest } from '../../transport';
import { sessionIdField, profileNameField } from '../common/fields';

export const description: INodeProperties[] = [
	{
		displayName:
			"Note: This operation is not needed if you enabled 'Save Profile' in the 'Create Session' operation",
		name: 'notice',
		type: 'notice',
		displayOptions: {
			show: {
				resource: ['session'],
				operation: ['save'],
			},
		},
		default: 'This operation will save the profile on session termination',
	},
	{
		...sessionIdField,
		displayOptions: {
			show: {
				resource: ['session'],
				operation: ['save'],
			},
		},
	},
	{
		...profileNameField,
		required: true,
		description:
			'The name of the <a href="https://docs.airtop.ai/guides/how-to/saving-a-profile" target="_blank">Profile</a> to save',
		displayOptions: {
			show: {
				resource: ['session'],
				operation: ['save'],
			},
		},
		hint: 'Name of the profile you want to save. Must consist only of alphanumeric characters and hyphens "-"',
	},
];

export async function execute(
	this: IExecuteFunctions,
	index: number,
): Promise<INodeExecutionData[]> {
	const sessionId = validateSessionId.call(this, index);
	let profileName = validateRequiredStringField.call(this, index, 'profileName', 'Profile Name');
	profileName = validateProfileName.call(this, index);

	const response = await apiRequest.call(
		this,
		'PUT',
		`/sessions/${sessionId}/save-profile-on-termination/${profileName}`,
	);

	// validate response
	validateAirtopApiResponse(this.getNode(), response);

	return this.helpers.returnJsonArray({ sessionId, profileName, ...response } as IDataObject);
}
