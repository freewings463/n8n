"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/helpers/description.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/OpenAi 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:prettifyOperation、configureNodeInputs。关键函数/方法:prettifyOperation、capitalize、configureNodeInputs。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/helpers/description.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/OpenAi/helpers/description.py

import type { INodeInputConfiguration } from 'n8n-workflow';

export const prettifyOperation = (resource: string, operation: string) => {
	if (operation === 'deleteAssistant') {
		return 'Delete Assistant';
	}

	if (operation === 'deleteFile') {
		return 'Delete File';
	}

	if (operation === 'classify') {
		return 'Classify Text';
	}

	if (operation === 'message' && resource === 'text') {
		return 'Message Model';
	}

	const capitalize = (str: string) => {
		const chars = str.split('');
		chars[0] = chars[0].toUpperCase();
		return chars.join('');
	};

	if (['transcribe', 'translate'].includes(operation)) {
		resource = 'recording';
	}

	if (operation === 'list') {
		resource = resource + 's';
	}

	return `${capitalize(operation)} ${capitalize(resource)}`;
};

export const configureNodeInputs = (
	resource: string,
	operation: string,
	hideTools: string,
	memory: string | undefined,
) => {
	if (resource === 'assistant' && operation === 'message') {
		const inputs: INodeInputConfiguration[] = [
			{ type: 'main' },
			{ type: 'ai_tool', displayName: 'Tools' },
		];
		if (memory !== 'threadId') {
			inputs.push({ type: 'ai_memory', displayName: 'Memory', maxConnections: 1 });
		}
		return inputs;
	}
	if (resource === 'text' && (operation === 'message' || operation === 'response')) {
		if (hideTools === 'hide') {
			return ['main'];
		}
		return [{ type: 'main' }, { type: 'ai_tool', displayName: 'Tools' }];
	}

	return ['main'];
};
