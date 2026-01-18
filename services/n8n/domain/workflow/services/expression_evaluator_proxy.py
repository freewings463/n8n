"""
MIGRATION-META:
  source_path: packages/workflow/src/expression-evaluator-proxy.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src 的工作流评估器。导入/依赖:外部:无；内部:@n8n/tournament；本地:无。导出:setErrorHandler、evaluateExpression。关键函数/方法:setErrorHandler。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package workflow treated as domain model & rules
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/expression-evaluator-proxy.ts -> services/n8n/domain/workflow/services/expression_evaluator_proxy.py

import { Tournament } from '@n8n/tournament';

import {
	DollarSignValidator,
	FunctionThisSanitizer,
	PrototypeSanitizer,
} from './expression-sandboxing';

type Evaluator = (expr: string, data: unknown) => string | null | (() => unknown);
type ErrorHandler = (error: Error) => void;

const errorHandler: ErrorHandler = () => {};
const tournamentEvaluator = new Tournament(errorHandler, undefined, undefined, {
	before: [FunctionThisSanitizer],
	after: [PrototypeSanitizer, DollarSignValidator],
});
const evaluator: Evaluator = tournamentEvaluator.execute.bind(tournamentEvaluator);

export const setErrorHandler = (handler: ErrorHandler) => {
	tournamentEvaluator.errorHandler = handler;
};

export const evaluateExpression: Evaluator = (expr, data) => {
	return evaluator(expr, data);
};
