"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/PhilipsHue/PhilipsHue.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/PhilipsHue 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./GenericFunctions、./LightDescription。导出:PhilipsHue。关键函数/方法:execute、getLights。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/PhilipsHue/PhilipsHue.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/PhilipsHue/PhilipsHue_node.py

import type {
	IDataObject,
	IExecuteFunctions,
	ILoadOptionsFunctions,
	INodeExecutionData,
	INodePropertyOptions,
	INodeType,
	INodeTypeDescription,
} from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import { getUser, philipsHueApiRequest } from './GenericFunctions';
import { lightFields, lightOperations } from './LightDescription';

export class PhilipsHue implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Philips Hue',
		name: 'philipsHue',
		// eslint-disable-next-line n8n-nodes-base/node-class-description-icon-not-svg
		icon: 'file:philipshue.png',
		group: ['input'],
		version: 1,
		subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
		description: 'Consume Philips Hue API',
		defaults: {
			name: 'Philips Hue',
		},
		usableAsTool: true,
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'philipsHueOAuth2Api',
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
						name: 'Light',
						value: 'light',
					},
				],
				default: 'light',
			},
			...lightOperations,
			...lightFields,
		],
	};

	methods = {
		loadOptions: {
			// Get all the lights to display them to user so that they can
			// select them easily
			async getLights(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
				const returnData: INodePropertyOptions[] = [];

				const user = await getUser.call(this);

				const lights = await philipsHueApiRequest.call(this, 'GET', `/api/${user}/lights`);

				const groups = await philipsHueApiRequest.call(this, 'GET', `/api/${user}/groups`);

				for (const light of Object.keys(lights as IDataObject)) {
					let lightName = lights[light].name;
					const lightId = light;

					for (const groupId of Object.keys(groups as IDataObject)) {
						if (groups[groupId].type === 'Room' && groups[groupId].lights.includes(lightId)) {
							lightName = `${groups[groupId].name}: ${lightName}`;
						}
					}

					returnData.push({
						name: lightName,
						value: lightId,
					});
				}
				return returnData;
			},
		},
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();
		const returnData: INodeExecutionData[] = [];
		const length = items.length;
		let responseData;
		const resource = this.getNodeParameter('resource', 0);
		const operation = this.getNodeParameter('operation', 0);
		for (let i = 0; i < length; i++) {
			if (resource === 'light') {
				if (operation === 'update') {
					const lightId = this.getNodeParameter('lightId', i) as string;

					const on = this.getNodeParameter('on', i) as boolean;

					const additionalFields = this.getNodeParameter('additionalFields', i);

					const body = {
						on,
					};

					if (additionalFields.transitiontime) {
						additionalFields.transitiontime = (additionalFields.transitiontime as number) * 100;
					}

					if (additionalFields.xy) {
						additionalFields.xy = (additionalFields.xy as string)
							.split(',')
							.map((e: string) => parseFloat(e));
					}

					if (additionalFields.xy_inc) {
						additionalFields.xy_inc = (additionalFields.xy_inc as string)
							.split(',')
							.map((e: string) => parseFloat(e));
					}

					Object.assign(body, additionalFields);

					const user = await getUser.call(this);

					const data = await philipsHueApiRequest.call(
						this,
						'PUT',
						`/api/${user}/lights/${lightId}/state`,
						body,
					);

					responseData = {};

					for (const response of data) {
						Object.assign(responseData, response.success);
					}
				}
				if (operation === 'delete') {
					const lightId = this.getNodeParameter('lightId', i) as string;

					const user = await getUser.call(this);

					responseData = await philipsHueApiRequest.call(
						this,
						'DELETE',
						`/api/${user}/lights/${lightId}`,
					);
				}
				if (operation === 'getAll') {
					const returnAll = this.getNodeParameter('returnAll', i);

					const user = await getUser.call(this);

					const lights = await philipsHueApiRequest.call(this, 'GET', `/api/${user}/lights`);

					responseData = Object.values(lights as IDataObject);

					if (!returnAll) {
						const limit = this.getNodeParameter('limit', i);
						responseData = responseData.splice(0, limit);
					}
				}
				if (operation === 'get') {
					const lightId = this.getNodeParameter('lightId', i) as string;

					const user = await getUser.call(this);

					responseData = await philipsHueApiRequest.call(
						this,
						'GET',
						`/api/${user}/lights/${lightId}`,
					);
				}
			}
			const executionData = this.helpers.constructExecutionMetaData(
				this.helpers.returnJsonArray(responseData as IDataObject[]),
				{ itemData: { item: i } },
			);
			returnData.push(...executionData);
		}
		return [returnData];
	}
}
