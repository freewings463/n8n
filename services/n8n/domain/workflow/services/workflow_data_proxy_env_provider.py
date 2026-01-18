"""
MIGRATION-META:
  source_path: packages/workflow/src/workflow-data-proxy-env-provider.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src 的工作流模块。导入/依赖:外部:无；内部:无；本地:./errors/expression.error。导出:EnvProviderState、createEnvProviderState、createEnvProvider。关键函数/方法:get、createEnvProviderState、createEnvProvider、has。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package workflow treated as domain model & rules
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/workflow-data-proxy-env-provider.ts -> services/n8n/domain/workflow/services/workflow_data_proxy_env_provider.py

import { ExpressionError } from './errors/expression.error';

export type EnvProviderState = {
	isProcessAvailable: boolean;
	isEnvAccessBlocked: boolean;
	env: Record<string, string>;
};

/**
 * Captures a snapshot of the environment variables and configuration
 * that can be used to initialize an environment provider.
 */
export function createEnvProviderState(): EnvProviderState {
	const isProcessAvailable = typeof process !== 'undefined';
	const isEnvAccessBlocked = isProcessAvailable
		? process.env.N8N_BLOCK_ENV_ACCESS_IN_NODE !== 'false'
		: false;
	const env: Record<string, string> =
		!isProcessAvailable || isEnvAccessBlocked ? {} : (process.env as Record<string, string>);

	return {
		isProcessAvailable,
		isEnvAccessBlocked,
		env,
	};
}

/**
 * Creates a proxy that provides access to the environment variables
 * in the `WorkflowDataProxy`. Use the `createEnvProviderState` to
 * create the default state object that is needed for the proxy,
 * unless you need something specific.
 *
 * @example
 * createEnvProvider(
 *   runIndex,
 *   itemIndex,
 *   createEnvProviderState(),
 * )
 */
export function createEnvProvider(
	runIndex: number,
	itemIndex: number,
	providerState: EnvProviderState,
): Record<string, string> {
	return new Proxy(
		{},
		{
			has() {
				return true;
			},

			get(_, name) {
				if (name === 'isProxy') return true;

				if (!providerState.isProcessAvailable) {
					throw new ExpressionError('not accessible via UI, please run node', {
						runIndex,
						itemIndex,
					});
				}
				if (providerState.isEnvAccessBlocked) {
					throw new ExpressionError('access to env vars denied', {
						causeDetailed:
							'If you need access please contact the administrator to remove the environment variable ‘N8N_BLOCK_ENV_ACCESS_IN_NODE‘',
						runIndex,
						itemIndex,
					});
				}

				return providerState.env[name.toString()];
			},
		},
	);
}
