"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/llms/LMChatOpenAi/methods/loadModels.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/llms/LMChatOpenAi 的节点。导入/依赖:外部:openai、@utils/httpProxyAgent；内部:n8n-workflow、@n8n/di、@n8n/config；本地:../helpers/modelFiltering。导出:无。关键函数/方法:searchModels。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/llms/LMChatOpenAi/methods/loadModels.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/llms/LMChatOpenAi/methods/loadModels.py

import type { ILoadOptionsFunctions, INodeListSearchResult } from 'n8n-workflow';
import OpenAI from 'openai';

import { shouldIncludeModel } from '../../../vendors/OpenAi/helpers/modelFiltering';
import { getProxyAgent } from '@utils/httpProxyAgent';
import { Container } from '@n8n/di';
import { AiConfig } from '@n8n/config';

export async function searchModels(
	this: ILoadOptionsFunctions,
	filter?: string,
): Promise<INodeListSearchResult> {
	const credentials = await this.getCredentials('openAiApi');
	const baseURL =
		(this.getNodeParameter('options.baseURL', '') as string) ||
		(credentials.url as string) ||
		'https://api.openai.com/v1';
	const { openAiDefaultHeaders: defaultHeaders } = Container.get(AiConfig);

	const openai = new OpenAI({
		baseURL,
		apiKey: credentials.apiKey as string,
		fetchOptions: {
			dispatcher: getProxyAgent(baseURL),
		},
		defaultHeaders,
	});
	const { data: models = [] } = await openai.models.list();

	const url = baseURL && new URL(baseURL);
	const isCustomAPI = !!(url && !['api.openai.com', 'ai-assistant.n8n.io'].includes(url.hostname));

	const filteredModels = models.filter((model: { id: string }) => {
		const includeModel = shouldIncludeModel(model.id, isCustomAPI);

		if (!filter) return includeModel;

		return includeModel && model.id.toLowerCase().includes(filter.toLowerCase());
	});

	filteredModels.sort((a, b) => a.id.localeCompare(b.id));

	return {
		results: filteredModels.map((model: { id: string }) => ({
			name: model.id,
			value: model.id,
		})),
	};
}
