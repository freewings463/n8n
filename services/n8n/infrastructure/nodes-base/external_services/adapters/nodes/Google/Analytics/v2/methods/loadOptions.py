"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Analytics/v2/methods/loadOptions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Analytics 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../helpers/utils、../transport。导出:无。关键函数/方法:getDimensions、getMetrics、getViews、getProperties、getDimensionsGA4、getMetricsGA4。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Analytics/v2/methods/loadOptions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Analytics/v2/methods/loadOptions.py

import type { ILoadOptionsFunctions, INodePropertyOptions } from 'n8n-workflow';

import { sortLoadOptions } from '../helpers/utils';
import { googleApiRequest } from '../transport';

export async function getDimensions(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
	const returnData: INodePropertyOptions[] = [];
	const { items: dimensions } = await googleApiRequest.call(
		this,
		'GET',
		'',
		{},
		{},
		'https://www.googleapis.com/analytics/v3/metadata/ga/columns',
	);

	for (const dimension of dimensions) {
		if (dimension.attributes.type === 'DIMENSION' && dimension.attributes.status !== 'DEPRECATED') {
			returnData.push({
				name: dimension.attributes.uiName,
				value: dimension.id,
				description: dimension.attributes.description,
			});
		}
	}
	return sortLoadOptions(returnData);
}

export async function getMetrics(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
	const returnData: INodePropertyOptions[] = [];
	const { items: metrics } = await googleApiRequest.call(
		this,
		'GET',
		'',
		{},
		{},
		'https://www.googleapis.com/analytics/v3/metadata/ga/columns',
	);

	for (const metric of metrics) {
		if (metric.attributes.type === 'METRIC' && metric.attributes.status !== 'DEPRECATED') {
			returnData.push({
				name: metric.attributes.uiName,
				value: metric.id,
				description: metric.attributes.description,
			});
		}
	}
	return sortLoadOptions(returnData);
}

export async function getViews(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
	const returnData: INodePropertyOptions[] = [];
	const { items } = await googleApiRequest.call(
		this,
		'GET',
		'',
		{},
		{},
		'https://www.googleapis.com/analytics/v3/management/accounts/~all/webproperties/~all/profiles',
	);

	for (const item of items) {
		returnData.push({
			name: item.name,
			value: item.id,
			description: item.websiteUrl,
		});
	}

	return sortLoadOptions(returnData);
}

export async function getProperties(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
	const returnData: INodePropertyOptions[] = [];

	const { accounts } = await googleApiRequest.call(
		this,
		'GET',
		'',
		{},
		{},
		'https://analyticsadmin.googleapis.com/v1alpha/accounts',
	);

	for (const acount of accounts || []) {
		const { properties } = await googleApiRequest.call(
			this,
			'GET',
			'',
			{},
			{ filter: `parent:${acount.name}` },
			'https://analyticsadmin.googleapis.com/v1alpha/properties',
		);

		if (properties && properties.length > 0) {
			for (const property of properties) {
				const name = property.displayName;
				const value = property.name.split('/')[1] || property.name;
				returnData.push({ name, value });
			}
		}
	}
	return sortLoadOptions(returnData);
}

export async function getDimensionsGA4(
	this: ILoadOptionsFunctions,
): Promise<INodePropertyOptions[]> {
	const returnData: INodePropertyOptions[] = [];
	const propertyId = this.getNodeParameter('propertyId', undefined, {
		extractValue: true,
	}) as string;
	const { dimensions } = await googleApiRequest.call(
		this,
		'GET',
		`/v1beta/properties/${propertyId}/metadata`,
		{},
		{ fields: 'dimensions' },
	);

	for (const dimension of dimensions) {
		returnData.push({
			name: dimension.uiName as string,
			value: dimension.apiName as string,
			description: dimension.description as string,
		});
	}
	return sortLoadOptions(returnData);
}

export async function getMetricsGA4(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
	const returnData: INodePropertyOptions[] = [];
	const propertyId = this.getNodeParameter('propertyId', undefined, {
		extractValue: true,
	}) as string;
	const { metrics } = await googleApiRequest.call(
		this,
		'GET',
		`/v1beta/properties/${propertyId}/metadata`,
		{},
		{ fields: 'metrics' },
	);

	for (const metric of metrics) {
		returnData.push({
			name: metric.uiName as string,
			value: metric.apiName as string,
			description: metric.description as string,
		});
	}
	return sortLoadOptions(returnData);
}
