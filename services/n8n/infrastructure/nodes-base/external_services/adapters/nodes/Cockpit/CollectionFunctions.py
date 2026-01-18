"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Cockpit/CollectionFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Cockpit 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./CollectionInterface、./GenericFunctions。导出:无。关键函数/方法:createCollectionEntry、getAllCollectionEntries、fields、getAllCollectionNames。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Cockpit/CollectionFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Cockpit/CollectionFunctions.py

import type { IExecuteFunctions, ILoadOptionsFunctions, IDataObject } from 'n8n-workflow';
import { jsonParse } from 'n8n-workflow';

import type { ICollection } from './CollectionInterface';
import { cockpitApiRequest } from './GenericFunctions';

export async function createCollectionEntry(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	resourceName: string,
	data: IDataObject,
	id?: string,
): Promise<any> {
	const body: ICollection = {
		data,
	};

	if (id) {
		body.data = {
			_id: id,
			...body.data,
		};
	}

	return await cockpitApiRequest.call(this, 'POST', `/collections/save/${resourceName}`, body);
}

export async function getAllCollectionEntries(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	resourceName: string,
	options: IDataObject,
): Promise<any> {
	const body: ICollection = {};

	if (options.fields) {
		const fields = (options.fields as string).split(',').map((field) => field.trim());

		const bodyFields = {
			_id: false,
		} as IDataObject;
		for (const field of fields) {
			bodyFields[field] = true;
		}

		body.fields = bodyFields;
	}

	if (options.filter) {
		body.filter = jsonParse(options.filter.toString(), {
			errorMessage: "'Filter' option is not valid JSON",
		});
	}

	if (options.limit) {
		body.limit = options.limit as number;
	}

	if (options.skip) {
		body.skip = options.skip as number;
	}

	if (options.sort) {
		body.sort = jsonParse(options.sort.toString(), {
			errorMessage: "'Sort' option is not valid JSON",
		});
	}

	if (options.populate) {
		body.populate = options.populate as boolean;
	}

	body.simple = true;
	if (options.rawData) {
		body.simple = !options.rawData;
	}

	if (options.language) {
		body.lang = options.language as string;
	}

	return await cockpitApiRequest.call(this, 'POST', `/collections/get/${resourceName}`, body);
}

export async function getAllCollectionNames(
	this: IExecuteFunctions | ILoadOptionsFunctions,
): Promise<string[]> {
	return await cockpitApiRequest.call(this, 'GET', '/collections/listCollections', {});
}
