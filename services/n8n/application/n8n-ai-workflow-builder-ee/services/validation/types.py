"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/validation/types.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/validation 的工作流类型。导入/依赖:外部:无；内部:n8n-workflow、@/types；本地:无。导出:ProgrammaticViolationType、PROGRAMMATIC_VIOLATION_NAMES、ProgrammaticViolationName、TelemetryValidationStatus、ProgrammaticViolation、SingleEvaluatorResult、ProgrammaticChecksResult、ProgrammaticEvaluationResult 等2项。关键函数/方法:无。用于定义工作流相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/validation/types.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/validation/types.py

import type { INodeTypeDescription, NodeConnectionType } from 'n8n-workflow';

import type { SimpleWorkflow } from '@/types';

export type ProgrammaticViolationType = 'critical' | 'major' | 'minor';

export const PROGRAMMATIC_VIOLATION_NAMES = [
	'tool-node-has-no-parameters',
	// this validation has been removed for now as it was throwing a lot of false positives
	'tool-node-static-parameters',
	'agent-static-prompt',
	'agent-no-system-prompt',
	'non-tool-node-uses-fromai',
	'workflow-has-no-nodes',
	'workflow-has-no-trigger',
	'workflow-exceeds-max-nodes-limit',
	'node-missing-required-input',
	'node-unsupported-connection-input',
	'node-merge-single-input',
	'node-merge-incorrect-num-inputs',
	'node-merge-missing-input',
	'sub-node-not-connected',
	'node-type-not-found',
	'failed-to-resolve-connections',
	'workflow-similarity-node-insert',
	'workflow-similarity-node-delete',
	'workflow-similarity-node-substitute',
	'workflow-similarity-edge-insert',
	'workflow-similarity-edge-delete',
	'workflow-similarity-edge-substitute',
	'workflow-similarity-evaluation-failed',
	'http-request-hardcoded-credentials',
	'set-node-credential-field',
] as const;

export type ProgrammaticViolationName = (typeof PROGRAMMATIC_VIOLATION_NAMES)[number];

export type TelemetryValidationStatus = Record<ProgrammaticViolationName, 'pass' | 'fail'>;

export interface ProgrammaticViolation {
	name: ProgrammaticViolationName;
	type: ProgrammaticViolationType;
	description: string;
	pointsDeducted: number;
}

export interface SingleEvaluatorResult {
	violations: ProgrammaticViolation[];
	score: number;
}

export interface ProgrammaticChecksResult {
	connections: ProgrammaticViolation[];
	nodes: ProgrammaticViolation[];
	trigger: ProgrammaticViolation[];
	agentPrompt: ProgrammaticViolation[];
	tools: ProgrammaticViolation[];
	fromAi: ProgrammaticViolation[];
	credentials: ProgrammaticViolation[];
}

export interface ProgrammaticEvaluationResult {
	overallScore: number;
	connections: SingleEvaluatorResult;
	nodes: SingleEvaluatorResult;
	trigger: SingleEvaluatorResult;
	agentPrompt: SingleEvaluatorResult;
	tools: SingleEvaluatorResult;
	fromAi: SingleEvaluatorResult;
	credentials: SingleEvaluatorResult;
	similarity: SingleEvaluatorResult | null;
}

export interface ProgrammaticEvaluationInput {
	generatedWorkflow: SimpleWorkflow;
	userPrompt?: string;
	referenceWorkflow?: SimpleWorkflow;
	referenceWorkflows?: SimpleWorkflow[];
	preset?: 'strict' | 'standard' | 'lenient';
}

export interface NodeResolvedConnectionTypesInfo {
	node: SimpleWorkflow['nodes'][0];
	nodeType: INodeTypeDescription;
	resolvedInputs?: Array<{ type: NodeConnectionType; required: boolean }>;
	resolvedOutputs?: Set<NodeConnectionType>;
}
