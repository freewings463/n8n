"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/GoogleGemini/methods/listSearch.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/GoogleGemini 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../transport。导出:无。关键函数/方法:baseModelSearch、response、modelSearch、audioModelSearch、imageGenerationModelSearch、imageEditModelSearch、videoGenerationModelSearch。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/GoogleGemini/methods/listSearch.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/GoogleGemini/methods/listSearch.py

import type { ILoadOptionsFunctions, INodeListSearchResult } from 'n8n-workflow';

import { apiRequest } from '../transport';

async function baseModelSearch(
	this: ILoadOptionsFunctions,
	modelFilter: (model: string) => boolean,
	filter?: string,
): Promise<INodeListSearchResult> {
	const response = (await apiRequest.call(this, 'GET', '/v1beta/models', {
		qs: {
			pageSize: 1000,
		},
	})) as {
		models: Array<{ name: string }>;
	};

	let models = response.models.filter((model) => modelFilter(model.name));
	if (filter) {
		models = models.filter((model) => model.name.toLowerCase().includes(filter.toLowerCase()));
	}

	return {
		results: models.map((model) => ({ name: model.name, value: model.name })),
	};
}

export async function modelSearch(
	this: ILoadOptionsFunctions,
	filter?: string,
): Promise<INodeListSearchResult> {
	return await baseModelSearch.call(
		this,
		(model) =>
			!model.includes('embedding') &&
			!model.includes('aqa') &&
			!model.includes('image') &&
			!model.includes('vision') &&
			!model.includes('veo') &&
			!model.includes('audio') &&
			!model.includes('tts'),
		filter,
	);
}

export async function audioModelSearch(
	this: ILoadOptionsFunctions,
	filter?: string,
): Promise<INodeListSearchResult> {
	return await baseModelSearch.call(
		this,
		(model) =>
			!model.includes('embedding') &&
			!model.includes('aqa') &&
			!model.includes('image') &&
			!model.includes('vision') &&
			!model.includes('veo') &&
			!model.includes('tts'), // we don't have a tts operation
		filter,
	);
}

export async function imageGenerationModelSearch(
	this: ILoadOptionsFunctions,
	filter?: string,
): Promise<INodeListSearchResult> {
	const rawResult = await baseModelSearch.call(this, (model) => model.includes('image'));
	let results = rawResult.results.map((r) => {
		if (r.name.includes('gemini-2.5-flash-image')) {
			return { name: `${r.name} (Nano Banana)`, value: r.value };
		}

		if (r.name.includes('gemini-3-pro-image')) {
			return { name: `${r.name} (Nano Banana Pro)`, value: r.value };
		}

		return r;
	});

	if (filter) {
		const filterLowerCase = filter.toLowerCase();
		results = results.filter((r) => r.name.toLowerCase().includes(filterLowerCase));
	}

	return {
		results,
	};
}

export async function imageEditModelSearch(
	this: ILoadOptionsFunctions,
	filter?: string,
): Promise<INodeListSearchResult> {
	const result = await imageGenerationModelSearch.call(this, filter);
	return {
		results: result.results.filter((r) => r.name.toLowerCase().includes('nano banana')),
	};
}

export async function videoGenerationModelSearch(
	this: ILoadOptionsFunctions,
	filter?: string,
): Promise<INodeListSearchResult> {
	return await baseModelSearch.call(this, (model) => model.includes('veo'), filter);
}
