"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Clearbit/Clearbit.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Clearbit 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./CompanyDescription、./GenericFunctions、./PersonDescription。导出:Clearbit。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Clearbit/Clearbit.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Clearbit/Clearbit_node.py

import type {
	IExecuteFunctions,
	IDataObject,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
} from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import { companyFields, companyOperations } from './CompanyDescription';
import { clearbitApiRequest } from './GenericFunctions';
import { personFields, personOperations } from './PersonDescription';

export class Clearbit implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Clearbit',
		name: 'clearbit',
		icon: 'file:clearbit.svg',
		group: ['output'],
		version: 1,
		subtitle: '={{$parameter["operation"] + ":" + $parameter["resource"]}}',
		description: 'Consume Clearbit API',
		defaults: {
			name: 'Clearbit',
		},
		usableAsTool: true,
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'clearbitApi',
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
						name: 'Company',
						value: 'company',
						description: 'The Company API allows you to look up a company by their domain',
					},
					{
						name: 'Person',
						value: 'person',
						description:
							'The Person API lets you retrieve social information associated with an email address, such as a person’s name, location and Twitter handle',
					},
				],
				default: 'company',
			},
			...companyOperations,
			...companyFields,
			...personOperations,
			...personFields,
		],
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();
		const returnData: INodeExecutionData[] = [];
		const length = items.length;
		const qs: IDataObject = {};
		let responseData;
		const resource = this.getNodeParameter('resource', 0);
		const operation = this.getNodeParameter('operation', 0);
		for (let i = 0; i < length; i++) {
			try {
				if (resource === 'person') {
					if (operation === 'enrich') {
						const email = this.getNodeParameter('email', i) as string;
						const additionalFields = this.getNodeParameter('additionalFields', i);
						qs.email = email;
						if (additionalFields.givenName) {
							qs.given_name = additionalFields.givenName as string;
						}
						if (additionalFields.familyName) {
							qs.family_name = additionalFields.familyName as string;
						}
						if (additionalFields.ipAddress) {
							qs.ip_address = additionalFields.ipAddress as string;
						}
						if (additionalFields.location) {
							qs.location = additionalFields.location as string;
						}
						if (additionalFields.company) {
							qs.company = additionalFields.company as string;
						}
						if (additionalFields.companyDomain) {
							qs.company_domain = additionalFields.companyDomain as string;
						}
						if (additionalFields.linkedIn) {
							qs.linkedin = additionalFields.linkedIn as string;
						}
						if (additionalFields.twitter) {
							qs.twitter = additionalFields.twitter as string;
						}
						if (additionalFields.facebook) {
							qs.facebook = additionalFields.facebook as string;
						}
						responseData = await clearbitApiRequest.call(
							this,
							'GET',
							`${resource}-stream`,
							'/v2/people/find',
							{},
							qs,
						);
					}
				}
				if (resource === 'company') {
					if (operation === 'enrich') {
						const domain = this.getNodeParameter('domain', i) as string;
						const additionalFields = this.getNodeParameter('additionalFields', i);
						qs.domain = domain;
						if (additionalFields.companyName) {
							qs.company_name = additionalFields.companyName as string;
						}
						if (additionalFields.linkedin) {
							qs.linkedin = additionalFields.linkedin as string;
						}
						if (additionalFields.twitter) {
							qs.twitter = additionalFields.twitter as string;
						}
						if (additionalFields.facebook) {
							qs.facebook = additionalFields.facebook as string;
						}
						responseData = await clearbitApiRequest.call(
							this,
							'GET',
							`${resource}-stream`,
							'/v2/companies/find',
							{},
							qs,
						);
					}
					if (operation === 'autocomplete') {
						const name = this.getNodeParameter('name', i) as string;
						qs.query = name;
						responseData = await clearbitApiRequest.call(
							this,
							'GET',
							'autocomplete',
							'/v1/companies/suggest',
							{},
							qs,
						);
					}
				}
				const executionData = this.helpers.constructExecutionMetaData(
					this.helpers.returnJsonArray(responseData as IDataObject),
					{ itemData: { item: i } },
				);
				returnData.push(...executionData);
			} catch (error) {
				if (this.continueOnFail()) {
					returnData.push({ error: error.message, json: {} });
					continue;
				}
				throw error;
			}
		}
		return [returnData];
	}
}
