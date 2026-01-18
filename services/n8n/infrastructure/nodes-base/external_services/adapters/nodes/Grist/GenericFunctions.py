"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Grist/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Grist 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:parseSortProperties、isSafeInteger、parseFilterProperties、parseDefinedFields、parseAutoMappedInputs、throwOnZeroDefinedFields。关键函数/方法:gristApiRequest、parseSortProperties、isSafeInteger、parseFilterProperties、parseDefinedFields、parseAutoMappedInputs、throwOnZeroDefinedFields。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Grist/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Grist/GenericFunctions.py

import type {
	IDataObject,
	IExecuteFunctions,
	IHttpRequestMethods,
	ILoadOptionsFunctions,
	IRequestOptions,
	JsonObject,
} from 'n8n-workflow';
import { NodeApiError, NodeOperationError } from 'n8n-workflow';

import type {
	GristCredentials,
	GristDefinedFields,
	GristFilterProperties,
	GristSortProperties,
} from './types';

export async function gristApiRequest(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject | number[] = {},
	qs: IDataObject = {},
) {
	const { apiKey, planType, customSubdomain, selfHostedUrl } =
		await this.getCredentials<GristCredentials>('gristApi');

	const gristapiurl =
		planType === 'free'
			? `https://docs.getgrist.com/api${endpoint}`
			: planType === 'paid'
				? `https://${customSubdomain}.getgrist.com/api${endpoint}`
				: `${selfHostedUrl}/api${endpoint}`;

	const options: IRequestOptions = {
		headers: {
			Authorization: `Bearer ${apiKey}`,
		},
		method,
		uri: gristapiurl,
		qs,
		body,
		json: true,
	};

	if (!Object.keys(body).length) {
		delete options.body;
	}

	if (!Object.keys(qs).length) {
		delete options.qs;
	}

	try {
		return await this.helpers.request(options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export function parseSortProperties(sortProperties: GristSortProperties) {
	return sortProperties.reduce((acc, cur, curIdx) => {
		if (cur.direction === 'desc') acc += '-';
		acc += cur.field;
		if (curIdx !== sortProperties.length - 1) acc += ',';
		return acc;
	}, '');
}

export function isSafeInteger(val: number) {
	//used MIN_SAFE_INTEGER and MAX_SAFE_INTEGER instead of MIN_VALUE and MAX_VALUE to avoid edge cases
	return !isNaN(val) && val > Number.MIN_SAFE_INTEGER && val < Number.MAX_SAFE_INTEGER;
}

export function parseFilterProperties(filterProperties: GristFilterProperties) {
	return filterProperties.reduce<{ [key: string]: Array<string | number> }>((acc, cur) => {
		acc[cur.field] = acc[cur.field] ?? [];
		const values = isSafeInteger(Number(cur.values)) ? Number(cur.values) : cur.values;
		acc[cur.field].push(values);
		return acc;
	}, {});
}

export function parseDefinedFields(fieldsToSendProperties: GristDefinedFields) {
	return fieldsToSendProperties.reduce<{ [key: string]: string }>((acc, cur) => {
		acc[cur.fieldId] = cur.fieldValue;
		return acc;
	}, {});
}

export function parseAutoMappedInputs(incomingKeys: string[], inputsToIgnore: string[], item: any) {
	return incomingKeys.reduce<{ [key: string]: any }>((acc, curKey) => {
		if (inputsToIgnore.includes(curKey)) return acc;
		acc = { ...acc, [curKey]: item[curKey] };
		return acc;
	}, {});
}

export function throwOnZeroDefinedFields(this: IExecuteFunctions, fields: GristDefinedFields) {
	if (!fields?.length) {
		throw new NodeOperationError(
			this.getNode(),
			"No defined data found. Please specify the data to send in 'Fields to Send'.",
		);
	}
}
