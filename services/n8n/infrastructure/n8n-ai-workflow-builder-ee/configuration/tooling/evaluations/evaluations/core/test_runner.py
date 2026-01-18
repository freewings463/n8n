"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/evaluations/core/test-runner.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/evaluations/core 的工作流模块。导入/依赖:外部:@langchain/core/…/chat_models；内部:n8n-workflow；本地:../src/workflow-builder-agent、../chains/workflow-evaluator、../programmatic/programmatic-evaluation 等5项。导出:createErrorResult、RunSingleTestOptions、initializeTestTracking。关键函数/方法:createErrorResult、runSingleTest、getChatPayload、initializeTestTracking。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI builder evaluation harness/scripts -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/evaluations/core/test-runner.ts -> services/n8n/infrastructure/n8n-ai-workflow-builder-ee/configuration/tooling/evaluations/evaluations/core/test_runner.py

import type { BaseChatModel } from '@langchain/core/language_models/chat_models';
import type { INodeTypeDescription } from 'n8n-workflow';

import type { BuilderFeatureFlags, WorkflowBuilderAgent } from '../../src/workflow-builder-agent';
import { evaluateWorkflow } from '../chains/workflow-evaluator';
import { programmaticEvaluation } from '../programmatic/programmatic-evaluation';
import type { EvaluationInput, TestCase } from '../types/evaluation';
import { isWorkflowStateValues, safeExtractUsage } from '../types/langsmith';
import type { TestResult } from '../types/test-result';
import { calculateCacheStats } from '../utils/cache-analyzer';
import { consumeGenerator, getChatPayload } from '../utils/evaluation-helpers';

/**
 * Creates an error result for a failed test
 * @param testCase - The test case that failed
 * @param error - The error that occurred
 * @returns TestResult with error information
 */
export function createErrorResult(testCase: TestCase, error: unknown): TestResult {
	const errorMessage = error instanceof Error ? error.message : String(error);

	return {
		testCase,
		generatedWorkflow: { nodes: [], connections: {}, name: 'Generated Workflow' },
		evaluationResult: {
			overallScore: 0,
			functionality: { score: 0, violations: [] },
			connections: { score: 0, violations: [] },
			expressions: { score: 0, violations: [] },
			nodeConfiguration: { score: 0, violations: [] },
			efficiency: {
				score: 0,
				violations: [],
				redundancyScore: 0,
				pathOptimization: 0,
				nodeCountEfficiency: 0,
			},
			dataFlow: {
				score: 0,
				violations: [],
			},
			maintainability: {
				score: 0,
				violations: [],
				nodeNamingQuality: 0,
				workflowOrganization: 0,
				modularity: 0,
			},
			bestPractices: {
				score: 0,
				violations: [],
				techniques: [],
			},
			structuralSimilarity: { score: 0, violations: [], applicable: false },
			summary: `Evaluation failed: ${errorMessage}`,
		},
		programmaticEvaluationResult: {
			overallScore: 0,
			connections: { violations: [], score: 0 },
			nodes: { violations: [], score: 0 },
			trigger: { violations: [], score: 0 },
			agentPrompt: { violations: [], score: 0 },
			tools: { violations: [], score: 0 },
			fromAi: { violations: [], score: 0 },
			credentials: { violations: [], score: 0 },
			similarity: null,
		},
		generationTime: 0,
		error: errorMessage,
	};
}

export interface RunSingleTestOptions {
	agent: WorkflowBuilderAgent;
	llm: BaseChatModel;
	testCase: TestCase;
	nodeTypes: INodeTypeDescription[];
	userId?: string;
	featureFlags?: BuilderFeatureFlags;
}

/**
 * Runs a single test case by generating a workflow and evaluating it
 * @param agent - The workflow builder agent to use
 * @param llm - Language model for evaluation
 * @param testCase - Test case to execute
 * @param nodeTypes - Array of node type descriptions
 * @params opts - userId, User ID for the session and featureFlags, Optional feature flags to pass to the agent
 * @returns Test result with generated workflow and evaluation
 */
export async function runSingleTest(
	agent: WorkflowBuilderAgent,
	llm: BaseChatModel,
	testCase: TestCase,
	nodeTypes: INodeTypeDescription[],
	opts?: { userId?: string; featureFlags?: BuilderFeatureFlags },
): Promise<TestResult> {
	const userId = opts?.userId ?? 'test-user';
	try {
		// Generate workflow
		const startTime = Date.now();
		await consumeGenerator(
			agent.chat(
				getChatPayload({
					evalType: 'single-eval',
					message: testCase.prompt,
					workflowId: testCase.id,
					featureFlags: opts?.featureFlags,
				}),
				userId,
			),
		);
		const generationTime = Date.now() - startTime;

		// Get generated workflow with validation
		const state = await agent.getState(testCase.id, userId);

		// Validate workflow state
		if (!state.values || !isWorkflowStateValues(state.values)) {
			throw new Error('Invalid workflow state: missing or malformed workflow');
		}

		const generatedWorkflow = state.values.workflowJSON;

		// Extract cache statistics from messages
		const usage = safeExtractUsage(state.values.messages);
		const cacheStats = calculateCacheStats(usage);

		// Evaluate
		const evaluationInput: EvaluationInput = {
			userPrompt: testCase.prompt,
			generatedWorkflow,
			referenceWorkflow: testCase.referenceWorkflow,
			referenceWorkflows: testCase.referenceWorkflows,
		};

		const evaluationResult = await evaluateWorkflow(llm, evaluationInput);
		const programmaticEvaluationResult = await programmaticEvaluation(evaluationInput, nodeTypes);

		return {
			testCase,
			generatedWorkflow,
			evaluationResult,
			programmaticEvaluationResult,
			generationTime,
			cacheStats,
		};
	} catch (error) {
		return createErrorResult(testCase, error);
	}
}

/**
 * Initialize test tracking map
 * @param testCases - Array of test cases
 * @returns Map of test ID to status
 */
export function initializeTestTracking(
	testCases: TestCase[],
): Record<string, 'pending' | 'pass' | 'fail'> {
	const tracking: Record<string, 'pending' | 'pass' | 'fail'> = {};
	for (const testCase of testCases) {
		tracking[testCase.id] = 'pending';
	}
	return tracking;
}
