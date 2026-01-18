"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/agents/Agent/Agent.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/agents/Agent 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./V1/AgentV1.node、./V2/AgentV2.node、./V3/AgentV3.node。导出:Agent。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/agents/Agent/Agent.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/agents/Agent/Agent_node.py

import type { INodeTypeBaseDescription, IVersionedNodeType } from 'n8n-workflow';
import { VersionedNodeType } from 'n8n-workflow';

import { AgentV1 } from './V1/AgentV1.node';
import { AgentV2 } from './V2/AgentV2.node';
import { AgentV3 } from './V3/AgentV3.node';

export class Agent extends VersionedNodeType {
	constructor() {
		const baseDescription: INodeTypeBaseDescription = {
			displayName: 'AI Agent',
			name: 'agent',
			icon: 'fa:robot',
			iconColor: 'black',
			group: ['transform'],
			description: 'Generates an action plan and executes it. Can use external tools.',
			codex: {
				alias: ['LangChain', 'Chat', 'Conversational', 'Plan and Execute', 'ReAct', 'Tools'],
				categories: ['AI'],
				subcategories: {
					AI: ['Agents', 'Root Nodes'],
				},
				resources: {
					primaryDocumentation: [
						{
							url: 'https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent/',
						},
					],
				},
			},
			defaultVersion: 3.1,
		};

		const nodeVersions: IVersionedNodeType['nodeVersions'] = {
			1: new AgentV1(baseDescription),
			1.1: new AgentV1(baseDescription),
			1.2: new AgentV1(baseDescription),
			1.3: new AgentV1(baseDescription),
			1.4: new AgentV1(baseDescription),
			1.5: new AgentV1(baseDescription),
			1.6: new AgentV1(baseDescription),
			1.7: new AgentV1(baseDescription),
			1.8: new AgentV1(baseDescription),
			1.9: new AgentV1(baseDescription),
			2: new AgentV2(baseDescription),
			2.1: new AgentV2(baseDescription),
			2.2: new AgentV2(baseDescription),
			2.3: new AgentV2(baseDescription),
			3: new AgentV3(baseDescription),
			3.1: new AgentV3(baseDescription),
			// IMPORTANT Reminder to update AgentTool
		};

		super(nodeVersions, baseDescription);
	}
}
