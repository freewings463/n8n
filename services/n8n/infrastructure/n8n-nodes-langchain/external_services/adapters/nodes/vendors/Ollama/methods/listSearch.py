"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/Ollama/methods/listSearch.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/Ollama 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../helpers/interfaces、../transport。导出:无。关键函数/方法:modelSearch。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/Ollama/methods/listSearch.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/Ollama/methods/listSearch.py

import type { ILoadOptionsFunctions, INodeListSearchResult } from 'n8n-workflow';

import type { OllamaTagsResponse } from '../helpers/interfaces';
import { apiRequest } from '../transport';

export async function modelSearch(
	this: ILoadOptionsFunctions,
	filter?: string,
): Promise<INodeListSearchResult> {
	const response: OllamaTagsResponse = await apiRequest.call(this, 'GET', '/api/tags');

	let models = response.models;

	if (filter) {
		models = models.filter((model) => model.name.toLowerCase().includes(filter.toLowerCase()));
	}

	return {
		results: models.map((model) => ({ name: model.name, value: model.name })),
	};
}
