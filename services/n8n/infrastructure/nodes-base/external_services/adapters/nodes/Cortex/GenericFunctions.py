"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Cortex/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Cortex 的节点。导入/依赖:外部:moment-timezone；内部:无；本地:无。导出:getEntityLabel、splitTags、prepareParameters。关键函数/方法:cortexApiRequest、getEntityLabel、splitTags、prepareParameters。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Cortex/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Cortex/GenericFunctions.py

import moment from 'moment-timezone';
import type {
	IDataObject,
	IExecuteFunctions,
	IHookFunctions,
	IHttpRequestMethods,
	ILoadOptionsFunctions,
	IRequestOptions,
} from 'n8n-workflow';

export async function cortexApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	resource: string,

	body: any = {},
	query: IDataObject = {},
	uri?: string,
	option: IDataObject = {},
): Promise<any> {
	const credentials = await this.getCredentials('cortexApi');

	let options: IRequestOptions = {
		headers: {},
		method,
		qs: query,
		uri: uri || `${credentials.host}/api${resource}`,
		body,
		json: true,
	};
	if (Object.keys(option).length !== 0) {
		options = Object.assign({}, options, option);
	}
	if (Object.keys(body as IDataObject).length === 0) {
		delete options.body;
	}
	if (Object.keys(query).length === 0) {
		delete options.qs;
	}

	return await this.helpers.requestWithAuthentication.call(this, 'cortexApi', options);
}

export function getEntityLabel(entity: IDataObject): string {
	let label = '';
	switch (entity._type) {
		case 'case':
			label = `#${entity.caseId} ${entity.title}`;
			break;
		case 'case_artifact':
			//@ts-ignore
			label = `[${entity.dataType}] ${entity.data ? entity.data : entity.attachment.name}`;
			break;
		case 'alert':
			label = `[${entity.source}:${entity.sourceRef}] ${entity.title}`;
			break;
		case 'case_task_log':
			label = `${entity.message} from ${entity.createdBy}`;
			break;
		case 'case_task':
			label = `${entity.title} (${entity.status})`;
			break;
		case 'job':
			label = `${entity.analyzerName} (${entity.status})`;
			break;
		default:
			break;
	}
	return label;
}

export function splitTags(tags: string): string[] {
	return tags.split(',').filter((tag) => tag !== ' ' && tag);
}

export function prepareParameters(values: IDataObject): IDataObject {
	const response: IDataObject = {};
	for (const key in values) {
		if (values[key] !== undefined && values[key] !== null && values[key] !== '') {
			if (moment(values[key] as string, moment.ISO_8601).isValid()) {
				response[key] = Date.parse(values[key] as string);
			} else if (key === 'tags') {
				response[key] = splitTags(values[key] as string);
			} else {
				response[key] = values[key];
			}
		}
	}
	return response;
}
