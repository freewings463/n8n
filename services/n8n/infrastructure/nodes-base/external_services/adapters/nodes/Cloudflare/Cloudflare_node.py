"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Cloudflare/Cloudflare.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Cloudflare 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./GenericFunctions、./ZoneCertificateDescription。导出:Cloudflare。关键函数/方法:execute、getZones。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Cloudflare/Cloudflare.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Cloudflare/Cloudflare_node.py

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

import { cloudflareApiRequest, cloudflareApiRequestAllItems } from './GenericFunctions';
import { zoneCertificateFields, zoneCertificateOperations } from './ZoneCertificateDescription';

export class Cloudflare implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Cloudflare',
		name: 'cloudflare',
		icon: 'file:cloudflare.svg',
		group: ['input'],
		version: 1,
		subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
		description: 'Consume Cloudflare API',
		defaults: {
			name: 'Cloudflare',
		},
		usableAsTool: true,
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'cloudflareApi',
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
						name: 'Zone Certificate',
						value: 'zoneCertificate',
					},
				],
				default: 'zoneCertificate',
			},
			...zoneCertificateOperations,
			...zoneCertificateFields,
		],
	};

	methods = {
		loadOptions: {
			async getZones(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
				const returnData: INodePropertyOptions[] = [];
				const { result: zones } = await cloudflareApiRequest.call(this, 'GET', '/zones');
				for (const zone of zones) {
					returnData.push({
						name: zone.name,
						value: zone.id,
					});
				}
				return returnData;
			},
		},
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();
		const returnData: IDataObject[] = [];
		const length = items.length;
		const qs: IDataObject = {};
		let responseData;
		const resource = this.getNodeParameter('resource', 0);
		const operation = this.getNodeParameter('operation', 0);

		for (let i = 0; i < length; i++) {
			try {
				if (resource === 'zoneCertificate') {
					//https://api.cloudflare.com/#zone-level-authenticated-origin-pulls-delete-certificate
					if (operation === 'delete') {
						const zoneId = this.getNodeParameter('zoneId', i) as string;
						const certificateId = this.getNodeParameter('certificateId', i) as string;

						responseData = await cloudflareApiRequest.call(
							this,
							'DELETE',
							`/zones/${zoneId}/origin_tls_client_auth/${certificateId}`,
							{},
						);
						responseData = responseData.result;
					}
					//https://api.cloudflare.com/#zone-level-authenticated-origin-pulls-get-certificate-details
					if (operation === 'get') {
						const zoneId = this.getNodeParameter('zoneId', i) as string;
						const certificateId = this.getNodeParameter('certificateId', i) as string;

						responseData = await cloudflareApiRequest.call(
							this,
							'GET',
							`/zones/${zoneId}/origin_tls_client_auth/${certificateId}`,
							{},
						);
						responseData = responseData.result;
					}
					//https://api.cloudflare.com/#zone-level-authenticated-origin-pulls-list-certificates
					if (operation === 'getMany') {
						const zoneId = this.getNodeParameter('zoneId', i) as string;
						const returnAll = this.getNodeParameter('returnAll', i);
						const filters = this.getNodeParameter('filters', i, {});

						Object.assign(qs, filters);

						if (returnAll) {
							responseData = await cloudflareApiRequestAllItems.call(
								this,
								'result',
								'GET',
								`/zones/${zoneId}/origin_tls_client_auth`,
								{},
								qs,
							);
						} else {
							const limit = this.getNodeParameter('limit', i);
							Object.assign(qs, { per_page: limit });
							responseData = await cloudflareApiRequest.call(
								this,
								'GET',
								`/zones/${zoneId}/origin_tls_client_auth`,
								{},
								qs,
							);
							responseData = responseData.result;
						}
					}
					//https://api.cloudflare.com/#zone-level-authenticated-origin-pulls-upload-certificate
					if (operation === 'upload') {
						const zoneId = this.getNodeParameter('zoneId', i) as string;
						const certificate = this.getNodeParameter('certificate', i) as string;
						const privateKey = this.getNodeParameter('privateKey', i) as string;

						const body: IDataObject = {
							certificate,
							private_key: privateKey,
						};

						responseData = await cloudflareApiRequest.call(
							this,
							'POST',
							`/zones/${zoneId}/origin_tls_client_auth`,
							body,
							qs,
						);

						responseData = responseData.result;
					}
				}

				returnData.push(
					...this.helpers.constructExecutionMetaData(
						this.helpers.returnJsonArray(responseData as IDataObject[]),
						{
							itemData: { item: i },
						},
					),
				);
			} catch (error) {
				if (this.continueOnFail()) {
					returnData.push({ json: { error: error.message } });
					continue;
				}
				throw error;
			}
		}

		return [returnData as INodeExecutionData[]];
	}
}
