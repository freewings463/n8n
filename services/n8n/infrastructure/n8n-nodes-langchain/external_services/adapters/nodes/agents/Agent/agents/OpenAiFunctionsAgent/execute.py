"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/OpenAiFunctionsAgent/execute.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/agents/Agent 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../V1/execute。导出:无。关键函数/方法:openAiFunctionsAgentExecute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/OpenAiFunctionsAgent/execute.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/agents/Agent/agents/OpenAiFunctionsAgent/execute.py

import type { IExecuteFunctions, INodeExecutionData } from 'n8n-workflow';

import { toolsAgentExecute } from '../ToolsAgent/V1/execute';

/**
 * OpenAI Functions Agent (legacy) - redirects to Tools Agent
 *
 * The OpenAI Functions Agent uses the legacy @langchain/classic API which has
 * compatibility issues with langchain 1.0. The Tools Agent uses the modern
 * createToolCallingAgent API which works correctly.
 *
 * Since both agents provide similar functionality (calling tools/functions),
 * we redirect to the Tools Agent implementation for better compatibility.
 */
export async function openAiFunctionsAgentExecute(
	this: IExecuteFunctions,
	_nodeVersion: number,
): Promise<INodeExecutionData[][]> {
	return await toolsAgentExecute.call(this);
}
