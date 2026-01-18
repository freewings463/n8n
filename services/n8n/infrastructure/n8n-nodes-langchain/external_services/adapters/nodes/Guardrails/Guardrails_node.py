"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/Guardrails/Guardrails.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/Guardrails 的节点。导入/依赖:外部:无；内部:无；本地:./v1/GuardrailsV1.node、./v2/GuardrailsV2.node。导出:Guardrails。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/Guardrails/Guardrails.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/Guardrails/Guardrails_node.py

import {
	VersionedNodeType,
	type INodeTypeBaseDescription,
	type IVersionedNodeType,
} from 'n8n-workflow';

import { GuardrailsV1 } from './v1/GuardrailsV1.node';
import { GuardrailsV2 } from './v2/GuardrailsV2.node';

export class Guardrails extends VersionedNodeType {
	constructor() {
		const baseDescription: INodeTypeBaseDescription = {
			displayName: 'Guardrails',
			name: 'guardrails',
			icon: 'file:guardrails.svg',
			group: ['transform'],
			defaultVersion: 2,
			description:
				'Safeguard AI models from malicious input or prevent them from generating undesirable responses',
			codex: {
				alias: ['LangChain', 'Guardrails', 'PII', 'Secret', 'Injection', 'Sanitize'],
				categories: ['AI'],
				subcategories: {
					AI: ['Agents', 'Miscellaneous', 'Root Nodes'],
				},
				resources: {
					primaryDocumentation: [
						{
							url: 'https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-langchain.guardrails/',
						},
					],
				},
			},
		};

		const nodeVersions: IVersionedNodeType['nodeVersions'] = {
			1: new GuardrailsV1(baseDescription),
			2: new GuardrailsV2(baseDescription),
		};

		super(nodeVersions, baseDescription);
	}
}
