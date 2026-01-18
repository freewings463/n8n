"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/utils/tracing.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/utils 的工具。导入/依赖:外部:@langchain/core/…/manager；内部:n8n-workflow；本地:无。导出:getTracingConfig。关键函数/方法:getTracingConfig。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Integration package defaulted to infrastructure/external_services
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/utils/tracing.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/utils/tracing.py

import type { BaseCallbackConfig } from '@langchain/core/callbacks/manager';
import type { IExecuteFunctions } from 'n8n-workflow';

interface TracingConfig {
	additionalMetadata?: Record<string, unknown>;
}

export function getTracingConfig(
	context: IExecuteFunctions,
	config: TracingConfig = {},
): BaseCallbackConfig {
	const parentRunManager = context.getParentCallbackManager
		? context.getParentCallbackManager()
		: undefined;

	return {
		runName: `[${context.getWorkflow().name}] ${context.getNode().name}`,
		metadata: {
			execution_id: context.getExecutionId(),
			workflow: context.getWorkflow(),
			node: context.getNode().name,
			...(config.additionalMetadata ?? {}),
		},
		callbacks: parentRunManager,
	};
}
