"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/OpenAi.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/OpenAi 的节点。导入/依赖:外部:无；内部:无；本地:./helpers/description、./v1/OpenAiV1.node、./v2/OpenAiV2.node。导出:OpenAi。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/OpenAi.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/OpenAi/OpenAi_node.py

import {
	type IVersionedNodeType,
	VersionedNodeType,
	type INodeTypeBaseDescription,
} from 'n8n-workflow';

import { prettifyOperation } from './helpers/description';
import { OpenAiV1 } from './v1/OpenAiV1.node';
import { OpenAiV2 } from './v2/OpenAiV2.node';

export class OpenAi extends VersionedNodeType {
	constructor() {
		const baseDescription: INodeTypeBaseDescription = {
			displayName: 'OpenAI',
			name: 'openAi',
			icon: { light: 'file:openAi.svg', dark: 'file:openAi.dark.svg' },
			group: ['transform'],
			defaultVersion: 2.1,
			subtitle: `={{(${prettifyOperation})($parameter.resource, $parameter.operation)}}`,
			description: 'Message an assistant or GPT, analyze images, generate audio, etc.',
			codex: {
				alias: [
					'LangChain',
					'ChatGPT',
					'Sora',
					'DallE',
					'whisper',
					'audio',
					'transcribe',
					'tts',
					'assistant',
				],
				categories: ['AI'],
				subcategories: {
					AI: ['Agents', 'Miscellaneous', 'Root Nodes'],
				},
				resources: {
					primaryDocumentation: [
						{
							url: 'https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-langchain.openai/',
						},
					],
				},
			},
		};

		const nodeVersions: IVersionedNodeType['nodeVersions'] = {
			1: new OpenAiV1(baseDescription),
			1.1: new OpenAiV1(baseDescription),
			1.2: new OpenAiV1(baseDescription),
			1.3: new OpenAiV1(baseDescription),
			1.4: new OpenAiV1(baseDescription),
			1.5: new OpenAiV1(baseDescription),
			1.6: new OpenAiV1(baseDescription),
			1.7: new OpenAiV1(baseDescription),
			1.8: new OpenAiV1(baseDescription),
			2: new OpenAiV2(baseDescription),
			2.1: new OpenAiV2(baseDescription),
		};

		super(nodeVersions, baseDescription);
	}
}
