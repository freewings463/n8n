"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Matrix/Matrix.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Matrix 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./AccountDescription、./EventDescription、./GenericFunctions、./MediaDescription 等3项。导出:Matrix。关键函数/方法:execute、getChannels。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Matrix/Matrix.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Matrix/Matrix_node.py

import type {
	IExecuteFunctions,
	IDataObject,
	ILoadOptionsFunctions,
	INodeExecutionData,
	INodePropertyOptions,
	INodeType,
	INodeTypeDescription,
} from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import { accountOperations } from './AccountDescription';
import { eventFields, eventOperations } from './EventDescription';
import { handleMatrixCall, matrixApiRequest } from './GenericFunctions';
import { mediaFields, mediaOperations } from './MediaDescription';
import { messageFields, messageOperations } from './MessageDescription';
import { roomFields, roomOperations } from './RoomDescription';
import { roomMemberFields, roomMemberOperations } from './RoomMemberDescription';

export class Matrix implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Matrix',
		name: 'matrix',
		// eslint-disable-next-line n8n-nodes-base/node-class-description-icon-not-svg
		icon: 'file:matrix.png',
		group: ['output'],
		version: 1,
		description: 'Consume Matrix API',
		subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
		defaults: {
			name: 'Matrix',
		},
		usableAsTool: true,
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'matrixApi',
				required: true,
			},
		],
		properties: [
			{
				displayName: 'Resource',
				name: 'resource',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Account',
						value: 'account',
					},
					{
						name: 'Event',
						value: 'event',
					},
					{
						name: 'Media',
						value: 'media',
					},
					{
						name: 'Message',
						value: 'message',
					},
					{
						name: 'Room',
						value: 'room',
					},
					{
						name: 'Room Member',
						value: 'roomMember',
					},
				],
				default: 'message',
			},
			...accountOperations,
			...eventOperations,
			...eventFields,
			...mediaOperations,
			...mediaFields,
			...messageOperations,
			...messageFields,
			...roomOperations,
			...roomFields,
			...roomMemberOperations,
			...roomMemberFields,
		],
	};

	methods = {
		loadOptions: {
			async getChannels(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
				const returnData: INodePropertyOptions[] = [];

				const joinedRoomsResponse = await matrixApiRequest.call(this, 'GET', '/joined_rooms');

				await Promise.all(
					joinedRoomsResponse.joined_rooms.map(async (roomId: string) => {
						try {
							const roomNameResponse = await matrixApiRequest.call(
								this,
								'GET',
								`/rooms/${roomId}/state/m.room.name`,
							);
							returnData.push({
								name: roomNameResponse.name,
								value: roomId,
							});
						} catch (error) {
							// TODO: Check, there is probably another way to get the name of this private-chats
							returnData.push({
								name: `Unknown: ${roomId}`,
								value: roomId,
							});
						}
					}),
				);

				returnData.sort((a, b) => {
					if (a.name < b.name) {
						return -1;
					}
					if (a.name > b.name) {
						return 1;
					}
					return 0;
				});

				return returnData;
			},
		},
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData() as IDataObject[];
		const returnData: INodeExecutionData[] = [];
		const resource = this.getNodeParameter('resource', 0);
		const operation = this.getNodeParameter('operation', 0);

		for (let i = 0; i < items.length; i++) {
			try {
				const responseData = await handleMatrixCall.call(this, i, resource, operation);
				const executionData = this.helpers.constructExecutionMetaData(
					this.helpers.returnJsonArray(responseData as IDataObject[]),
					{ itemData: { item: i } },
				);
				returnData.push(...executionData);
			} catch (error) {
				if (this.continueOnFail()) {
					const executionData = this.helpers.constructExecutionMetaData(
						this.helpers.returnJsonArray({ error: error.message }),
						{ itemData: { item: i } },
					);
					returnData.push(...executionData);
					continue;
				}
				throw error;
			}
		}
		return [returnData];
	}
}
