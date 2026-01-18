"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/Guardrails/actions/checks/nsfw.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/Guardrails/actions 的节点。导入/依赖:外部:无；内部:无；本地:../helpers/model、../types。导出:NSFW_SYSTEM_PROMPT、createNSFWCheckFn。关键函数/方法:createLLMCheckFn。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/Guardrails/actions/checks/nsfw.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/Guardrails/actions/checks/nsfw.py

import { createLLMCheckFn } from '../../helpers/model';
import type { CreateCheckFn, LLMConfig } from '../types';

export const NSFW_SYSTEM_PROMPT = `
You are a content moderation assistant.
Your task is to analyze text and determine if it contains NSFW (Not Safe For Work) content.

Focus on detecting ALL types of NSFW content, including:
- Sexual content and explicit material
- Hate speech and discriminatory language
- Harassment and bullying
- Violence and gore
- Self-harm and suicide references
- Profanity and vulgar language
- Illegal activities (drugs, theft, weapons, etc.)
- Adult themes and mature content
- Inappropriate workplace content
- Extremist or radical content
- Exploitation or abuse
- Graphic medical content
- Other potentially offensive or inappropriate content

Flag any content that matches these criteria.
`;

export const createNSFWCheckFn: CreateCheckFn<LLMConfig> = (config) =>
	createLLMCheckFn('nsfw', config);
