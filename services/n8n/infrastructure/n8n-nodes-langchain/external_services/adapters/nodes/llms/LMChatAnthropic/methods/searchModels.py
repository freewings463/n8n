"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/llms/LMChatAnthropic/methods/searchModels.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/llms/LMChatAnthropic 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:AnthropicModel。关键函数/方法:searchModels、response。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/llms/LMChatAnthropic/methods/searchModels.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/llms/LMChatAnthropic/methods/searchModels.py

import type {
	ILoadOptionsFunctions,
	INodeListSearchItems,
	INodeListSearchResult,
} from 'n8n-workflow';

export interface AnthropicModel {
	id: string;
	display_name: string;
	type: string;
	created_at: string;
}

export async function searchModels(
	this: ILoadOptionsFunctions,
	filter?: string,
): Promise<INodeListSearchResult> {
	const credentials = await this.getCredentials<{ url?: string }>('anthropicApi');

	const baseURL = credentials.url ?? 'https://api.anthropic.com';
	const response = (await this.helpers.httpRequestWithAuthentication.call(this, 'anthropicApi', {
		url: `${baseURL}/v1/models`,
		headers: {
			'anthropic-version': '2023-06-01',
		},
	})) as { data: AnthropicModel[] };

	const models = response.data || [];
	let results: INodeListSearchItems[] = [];

	if (filter) {
		for (const model of models) {
			if (model.id.toLowerCase().includes(filter.toLowerCase())) {
				results.push({
					name: model.display_name,
					value: model.id,
				});
			}
		}
	} else {
		results = models.map((model) => ({
			name: model.display_name,
			value: model.id,
		}));
	}

	// Sort models with more recent ones first (claude-3 before claude-2)
	results = results.sort((a, b) => {
		const modelA = models.find((m) => m.id === a.value);
		const modelB = models.find((m) => m.id === b.value);

		if (!modelA || !modelB) return 0;

		// Sort by created_at date, most recent first
		const dateA = new Date(modelA.created_at);
		const dateB = new Date(modelB.created_at);
		return dateB.getTime() - dateA.getTime();
	});

	return {
		results,
	};
}
