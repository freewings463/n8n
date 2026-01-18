"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/Guardrails/actions/checks/topicalAlignment.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/Guardrails/actions 的节点。导入/依赖:外部:无；内部:无；本地:../helpers/model、../types。导出:TOPICAL_ALIGNMENT_SYSTEM_PROMPT、createTopicalAlignmentCheckFn。关键函数/方法:createLLMCheckFn。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/Guardrails/actions/checks/topicalAlignment.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/Guardrails/actions/checks/topicalAlignment.py

import { createLLMCheckFn } from '../../helpers/model';
import type { CreateCheckFn, LLMConfig } from '../types';

export const TOPICAL_ALIGNMENT_SYSTEM_PROMPT = `You are a content analysis system that determines if text stays on topic.

BUSINESS SCOPE: [INSERT BUSINESS SCOPE HERE]

Determine if the text stays within the defined business scope. Flag any content
that strays from the allowed topics.`;

export const createTopicalAlignmentCheckFn: CreateCheckFn<LLMConfig> = (config) =>
	createLLMCheckFn('topicalAlignment', config);
