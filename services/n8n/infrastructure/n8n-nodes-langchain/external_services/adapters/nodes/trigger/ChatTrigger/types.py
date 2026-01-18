"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/trigger/ChatTrigger/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/trigger/ChatTrigger 的类型。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:AuthenticationChatOption、LoadPreviousSessionChatOption、assertValidLoadPreviousSessionOption。关键函数/方法:isValidLoadPreviousSessionOption、assertValidLoadPreviousSessionOption。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/trigger/ChatTrigger/types.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/trigger/ChatTrigger/types.py

import type { INode } from 'n8n-workflow';
import { NodeOperationError } from 'n8n-workflow';

const validOptions = ['notSupported', 'memory', 'manually'] as const;
export type AuthenticationChatOption = 'none' | 'basicAuth' | 'n8nUserAuth';
export type LoadPreviousSessionChatOption = (typeof validOptions)[number];

function isValidLoadPreviousSessionOption(value: unknown): value is LoadPreviousSessionChatOption {
	return typeof value === 'string' && (validOptions as readonly string[]).includes(value);
}

export function assertValidLoadPreviousSessionOption(
	value: string | undefined,
	node: INode,
): asserts value is LoadPreviousSessionChatOption | undefined {
	if (value && !isValidLoadPreviousSessionOption(value)) {
		throw new NodeOperationError(node, `Invalid loadPreviousSession option: ${value}`);
	}
}
