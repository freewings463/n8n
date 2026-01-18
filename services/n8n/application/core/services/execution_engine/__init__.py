"""
MIGRATION-META:
  source_path: packages/core/src/execution-engine/index.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/execution-engine 的执行入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./execution-lifecycle-hooks、./external-secrets-proxy。再导出:./active-workflows、./routing-node、./node-execution-context、./partial-execution-utils 等3项。导出:ExecutionLifecycleHooks、ExternalSecretsProxy、type IExternalSecretsManager、isEngineRequest。关键函数/方法:无。用于汇总导出并完成执行模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Core execution engine -> application/services/execution_engine
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/execution-engine/index.ts -> services/n8n/application/core/services/execution_engine/__init__.py

import type { DataTableProxyProvider, IExecutionContext, IWorkflowSettings } from 'n8n-workflow';

import type { ExecutionLifecycleHooks } from './execution-lifecycle-hooks';
import type { ExternalSecretsProxy } from './external-secrets-proxy';

declare module 'n8n-workflow' {
	interface IWorkflowExecuteAdditionalData {
		hooks?: ExecutionLifecycleHooks;
		externalSecretsProxy: ExternalSecretsProxy;
		'data-table'?: { dataTableProxyProvider: DataTableProxyProvider };
		// Project ID is currently only added on the additionalData if the user
		// has data table listing permission for that project. We should consider
		// that only data tables belonging to their respective projects are shown.
		dataTableProjectId?: string;
		/**
		 * Execution context for dynamic credential resolution (EE feature).
		 * Contains encrypted credential context that can be decrypted by resolvers.
		 */
		executionContext?: IExecutionContext;
		/**
		 * Workflow settings (EE feature).
		 * Contains workflow-level configuration including credential resolver ID.
		 */
		workflowSettings?: IWorkflowSettings;
	}
}

export * from './active-workflows';
export type * from './interfaces';
export * from './routing-node';
export * from './node-execution-context';
export * from './partial-execution-utils';
export * from './node-execution-context/utils/execution-metadata';
export * from './workflow-execute';
export * from './execution-context-hook-registry.service';
export { ExecutionLifecycleHooks } from './execution-lifecycle-hooks';
export { ExternalSecretsProxy, type IExternalSecretsManager } from './external-secrets-proxy';
export { isEngineRequest } from './requests-response';
