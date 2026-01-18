"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/chains/ChainSummarization/ChainSummarization.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/chains/ChainSummarization 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./V1/ChainSummarizationV1.node、./V2/ChainSummarizationV2.node。导出:ChainSummarization。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/chains/ChainSummarization/ChainSummarization.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/chains/ChainSummarization/ChainSummarization_node.py

import type { INodeTypeBaseDescription, IVersionedNodeType } from 'n8n-workflow';
import { VersionedNodeType } from 'n8n-workflow';

import { ChainSummarizationV1 } from './V1/ChainSummarizationV1.node';
import { ChainSummarizationV2 } from './V2/ChainSummarizationV2.node';

export class ChainSummarization extends VersionedNodeType {
	constructor() {
		const baseDescription: INodeTypeBaseDescription = {
			displayName: 'Summarization Chain',
			name: 'chainSummarization',
			icon: 'fa:link',
			iconColor: 'black',
			group: ['transform'],
			description: 'Transforms text into a concise summary',
			codex: {
				alias: ['LangChain'],
				categories: ['AI'],
				subcategories: {
					AI: ['Chains', 'Root Nodes'],
				},
				resources: {
					primaryDocumentation: [
						{
							url: 'https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.chainsummarization/',
						},
					],
				},
			},
			defaultVersion: 2.1,
		};

		const nodeVersions: IVersionedNodeType['nodeVersions'] = {
			1: new ChainSummarizationV1(baseDescription),
			2: new ChainSummarizationV2(baseDescription),
			2.1: new ChainSummarizationV2(baseDescription),
		};

		super(nodeVersions, baseDescription);
	}
}
