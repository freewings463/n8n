"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/Ollama/Ollama.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/Ollama 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./actions/router、./actions/versionDescription、./methods。导出:Ollama。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/Ollama/Ollama.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/Ollama/Ollama_node.py

import type { IExecuteFunctions, INodeType } from 'n8n-workflow';

import { router } from './actions/router';
import { versionDescription } from './actions/versionDescription';
import { listSearch } from './methods';

export class Ollama implements INodeType {
	description = versionDescription;

	methods = {
		listSearch,
	};

	async execute(this: IExecuteFunctions) {
		return await router.call(this);
	}
}
