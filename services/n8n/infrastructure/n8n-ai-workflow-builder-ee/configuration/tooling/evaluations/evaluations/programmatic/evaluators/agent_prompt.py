"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/evaluations/programmatic/evaluators/agent-prompt.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/evaluations/programmatic/evaluators 的工作流评估器。导入/依赖:外部:无；内部:@/types、@/validation/checks、@/validation/types；本地:../utils/score。导出:evaluateAgentPrompt。关键函数/方法:evaluateAgentPrompt。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI builder evaluation harness/scripts -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/evaluations/programmatic/evaluators/agent-prompt.ts -> services/n8n/infrastructure/n8n-ai-workflow-builder-ee/configuration/tooling/evaluations/evaluations/programmatic/evaluators/agent_prompt.py

import type { SimpleWorkflow } from '@/types';
import { validateAgentPrompt } from '@/validation/checks';
import type { SingleEvaluatorResult } from '@/validation/types';

import { calcSingleEvaluatorScore } from '../../utils/score';

export function evaluateAgentPrompt(workflow: SimpleWorkflow): SingleEvaluatorResult {
	const violations = validateAgentPrompt(workflow);

	return { violations, score: calcSingleEvaluatorScore({ violations }) };
}
