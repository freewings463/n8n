"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SeaTable/v2/actions/base/collaborator.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SeaTable/v2 的节点。导入/依赖:外部:无；内部:无；本地:../../GenericFunctions、../Interfaces。导出:properties、description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SeaTable/v2/actions/base/collaborator.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SeaTable/v2/actions/base/collaborator_operation.py

import {
	type IDataObject,
	type INodeExecutionData,
	type INodeProperties,
	type IExecuteFunctions,
	updateDisplayOptions,
} from 'n8n-workflow';

import { seaTableApiRequest } from '../../GenericFunctions';
import type { ICollaborator } from '../Interfaces';

export const properties: INodeProperties[] = [
	{
		displayName: 'Name or email of the collaborator',
		name: 'searchString',
		type: 'string',
		placeholder: 'Enter the name or the email or the collaborator',
		required: true,
		default: '',
		description:
			'SeaTable identifies users with a unique username like 244b43hr6fy54bb4afa2c2cb7369d244@auth.local. Get this username from an email or the name of a collaborator.',
	},
];

const displayOptions = {
	show: {
		resource: ['base'],
		operation: ['collaborator'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(
	this: IExecuteFunctions,
	index: number,
): Promise<INodeExecutionData[]> {
	const searchString = this.getNodeParameter('searchString', index) as string;

	const collaboratorsResult = await seaTableApiRequest.call(
		this,
		{},
		'GET',
		'/api-gateway/api/v2/dtables/{{dtable_uuid}}/related-users/',
	);
	const collaborators = collaboratorsResult.user_list || [];

	const data = collaborators.filter(
		(col: ICollaborator) =>
			col.contact_email.includes(searchString) || col.name.includes(searchString),
	);

	return this.helpers.returnJsonArray(data as IDataObject[]);
}
