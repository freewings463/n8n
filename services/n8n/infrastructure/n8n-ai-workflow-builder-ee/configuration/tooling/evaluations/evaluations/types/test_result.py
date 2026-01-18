"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/evaluations/types/test-result.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/evaluations/types 的工作流类型。导入/依赖:外部:无；内部:@/validation/types；本地:./evaluation、../types/workflow.js。导出:CacheStatistics、MessageCacheStats、TestResult。关键函数/方法:无。用于定义工作流相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI builder evaluation harness/scripts -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/evaluations/types/test-result.ts -> services/n8n/infrastructure/n8n-ai-workflow-builder-ee/configuration/tooling/evaluations/evaluations/types/test_result.py

import type { ProgrammaticEvaluationResult } from '@/validation/types';

import type { TestCase, EvaluationResult } from './evaluation';
import type { SimpleWorkflow } from '../../src/types/workflow.js';

export type {
	ProgrammaticEvaluationResult,
	SingleEvaluatorResult,
} from '@/validation/types';

/**
 * Cache statistics for prompt caching analysis
 */
export interface CacheStatistics {
	inputTokens: number;
	outputTokens: number;
	cacheCreationTokens: number;
	cacheReadTokens: number;
	cacheHitRate: number;
}

/**
 * Cache statistics for a single message/API call
 */
export interface MessageCacheStats {
	messageIndex: number;
	timestamp: string;
	messageType: 'user' | 'assistant' | 'tool_call' | 'tool_response';
	role?: string;
	toolName?: string;
	inputTokens: number;
	outputTokens: number;
	cacheCreationTokens: number;
	cacheReadTokens: number;
	cacheHitRate: number;
}

/**
 * Result of running a single test case
 */
export interface TestResult {
	testCase: TestCase;
	generatedWorkflow: SimpleWorkflow;
	evaluationResult: EvaluationResult;
	programmaticEvaluationResult: ProgrammaticEvaluationResult;
	generationTime: number;
	cacheStats?: CacheStatistics;
	error?: string;
}
