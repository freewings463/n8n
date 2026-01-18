"""
MIGRATION-META:
  source_path: packages/core/src/execution-engine/node-execution-context/utils/get-additional-keys.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/execution-engine/node-execution-context/utils 的执行工具。导入/依赖:外部:无；内部:n8n-workflow、@/constants；本地:./get-secrets-proxy。导出:getAdditionalKeys、getNonWorkflowAdditionalKeys。关键函数/方法:set、get、getAdditionalKeys、setWorkflowExecutionMetadata、setAll、setAllWorkflowExecutionMetadata、getAll、getNonWorkflowAdditionalKeys。用于提供执行通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Core execution engine -> application/services/execution_engine
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/execution-engine/node-execution-context/utils/get-additional-keys.ts -> services/n8n/application/core/services/execution_engine/node-execution-context/utils/get_additional_keys.py

import type {
	IRunExecutionData,
	IWorkflowDataProxyAdditionalKeys,
	IWorkflowExecuteAdditionalData,
	WorkflowExecuteMode,
} from 'n8n-workflow';
import { LoggerProxy } from 'n8n-workflow';

import { PLACEHOLDER_EMPTY_EXECUTION_ID } from '@/constants';

import {
	setWorkflowExecutionMetadata,
	setAllWorkflowExecutionMetadata,
	getWorkflowExecutionMetadata,
	getAllWorkflowExecutionMetadata,
} from './execution-metadata';
import { getSecretsProxy } from './get-secrets-proxy';

/** Returns the additional keys for Expressions and Function-Nodes */
export function getAdditionalKeys(
	additionalData: IWorkflowExecuteAdditionalData,
	mode: WorkflowExecuteMode,
	runExecutionData: IRunExecutionData | null,
	options?: { secretsEnabled?: boolean },
): IWorkflowDataProxyAdditionalKeys {
	const executionId = additionalData.executionId ?? PLACEHOLDER_EMPTY_EXECUTION_ID;
	const resumeUrl = `${additionalData.webhookWaitingBaseUrl}/${executionId}`;
	const resumeFormUrl = `${additionalData.formWaitingBaseUrl}/${executionId}`;
	return {
		$execution: {
			id: executionId,
			mode: mode === 'manual' ? 'test' : 'production',
			resumeUrl,
			resumeFormUrl,
			customData: runExecutionData
				? {
						set(key: string, value: string): void {
							try {
								setWorkflowExecutionMetadata(runExecutionData, key, value);
							} catch (e) {
								if (mode === 'manual') {
									throw e;
								}
								// eslint-disable-next-line @typescript-eslint/no-unsafe-argument, @typescript-eslint/no-unsafe-member-access
								LoggerProxy.debug(e.message);
							}
						},
						setAll(obj: Record<string, string>): void {
							try {
								setAllWorkflowExecutionMetadata(runExecutionData, obj);
							} catch (e) {
								if (mode === 'manual') {
									throw e;
								}
								// eslint-disable-next-line @typescript-eslint/no-unsafe-argument, @typescript-eslint/no-unsafe-member-access
								LoggerProxy.debug(e.message);
							}
						},
						get(key: string): string {
							return getWorkflowExecutionMetadata(runExecutionData, key);
						},
						getAll(): Record<string, string> {
							return getAllWorkflowExecutionMetadata(runExecutionData);
						},
					}
				: undefined,
		},
		$vars: additionalData.variables,
		$secrets: options?.secretsEnabled ? getSecretsProxy(additionalData) : undefined,

		// deprecated
		$executionId: executionId,
		$resumeWebhookUrl: resumeUrl,
	};
}

/**
 * Returns the global additional keys for Expressions
 * without workflow execution context
 * */
export function getNonWorkflowAdditionalKeys(
	additionalData: IWorkflowExecuteAdditionalData,
	options?: { secretsEnabled?: boolean },
): IWorkflowDataProxyAdditionalKeys {
	return {
		$vars: additionalData.variables,
		$secrets: options?.secretsEnabled ? getSecretsProxy(additionalData) : undefined,
	};
}
