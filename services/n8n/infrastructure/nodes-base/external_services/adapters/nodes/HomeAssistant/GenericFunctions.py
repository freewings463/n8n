"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/HomeAssistant/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/HomeAssistant 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:homeAssistantApiRequest、getHomeAssistantEntities、entityName、getHomeAssistantServices。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/HomeAssistant/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/HomeAssistant/GenericFunctions.py

import type {
	IExecuteFunctions,
	ILoadOptionsFunctions,
	IDataObject,
	INodePropertyOptions,
	JsonObject,
	IHttpRequestMethods,
	IRequestOptions,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

export async function homeAssistantApiRequest(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	resource: string,
	body: IDataObject = {},
	qs: IDataObject = {},
	uri?: string,
	option: IDataObject = {},
) {
	const credentials = await this.getCredentials('homeAssistantApi');

	let options: IRequestOptions = {
		headers: {
			Authorization: `Bearer ${credentials.accessToken}`,
		},
		method,
		qs,
		body,
		uri:
			uri ??
			`${credentials.ssl === true ? 'https' : 'http'}://${credentials.host}:${
				credentials.port
			}/api${resource}`,
		json: true,
	};

	options = Object.assign({}, options, option);
	if (Object.keys(options.body as IDataObject).length === 0) {
		delete options.body;
	}
	try {
		if (this.helpers.request) {
			return await this.helpers.request(options);
		}
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function getHomeAssistantEntities(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	domain = '',
) {
	const returnData: INodePropertyOptions[] = [];
	const entities = await homeAssistantApiRequest.call(this, 'GET', '/states');
	for (const entity of entities) {
		const entityId = entity.entity_id as string;
		if (domain === '' || (domain && entityId.startsWith(domain))) {
			const entityName = (entity.attributes.friendly_name as string) || entityId;
			returnData.push({
				name: entityName,
				value: entityId,
			});
		}
	}
	return returnData;
}

export async function getHomeAssistantServices(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	domain = '',
) {
	const returnData: INodePropertyOptions[] = [];
	const services = await homeAssistantApiRequest.call(this, 'GET', '/services');
	if (domain === '') {
		// If no domain specified return domains
		const domains = services.map(({ domain: service }: IDataObject) => service as string).sort();
		returnData.push(
			...(domains.map((service: string) => ({
				name: service,
				value: service,
			})) as INodePropertyOptions[]),
		);
		return returnData;
	} else {
		// If we have a domain, return all relevant services
		const domainServices = services.filter((service: IDataObject) => service.domain === domain);
		for (const domainService of domainServices) {
			for (const [serviceID, value] of Object.entries(domainService.services as IDataObject)) {
				const serviceProperties = value as IDataObject;
				const serviceName = serviceProperties.description || serviceID;
				returnData.push({
					name: serviceName as string,
					value: serviceID,
				});
			}
		}
	}
	return returnData;
}
