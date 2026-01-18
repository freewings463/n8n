"""
MIGRATION-META:
  source_path: packages/@n8n/config/src/configs/workflows.config.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/config/src/configs 的工作流配置。导入/依赖:外部:zod；内部:无；本地:../decorators。导出:WorkflowsConfig。关键函数/方法:无。用于集中定义工作流配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/config treated as infrastructure configuration/runtime environment
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/config/src/configs/workflows.config.ts -> services/n8n/infrastructure/n8n-config/configuration/configs/workflows_config.py

import { z } from 'zod';

import { Config, Env } from '../decorators';

const callerPolicySchema = z.enum(['any', 'none', 'workflowsFromAList', 'workflowsFromSameOwner']);
type CallerPolicy = z.infer<typeof callerPolicySchema>;

@Config
export class WorkflowsConfig {
	/** Default name for workflow */
	@Env('WORKFLOWS_DEFAULT_NAME')
	defaultName: string = 'My workflow';

	/** Default option for which workflows may call the current workflow */
	@Env('N8N_WORKFLOW_CALLER_POLICY_DEFAULT_OPTION', callerPolicySchema)
	callerPolicyDefaultOption: CallerPolicy = 'workflowsFromSameOwner';

	/** How many workflows to activate simultaneously during startup. */
	@Env('N8N_WORKFLOW_ACTIVATION_BATCH_SIZE')
	activationBatchSize: number = 1;

	/** Whether to enable workflow dependency indexing */
	@Env('N8N_WORKFLOWS_INDEXING_ENABLED')
	indexingEnabled: boolean = false;
}
