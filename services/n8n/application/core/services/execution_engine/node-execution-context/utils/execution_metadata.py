"""
MIGRATION-META:
  source_path: packages/core/src/execution-engine/node-execution-context/utils/execution-metadata.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/execution-engine/node-execution-context/utils 的执行工具。导入/依赖:外部:无；内部:n8n-workflow、@/errors/invalid-execution-metadata.error；本地:无。导出:KV_LIMIT、setWorkflowExecutionMetadata、setAllWorkflowExecutionMetadata、getAllWorkflowExecutionMetadata 等1项。关键函数/方法:setWorkflowExecutionMetadata、setAllWorkflowExecutionMetadata、getAllWorkflowExecutionMetadata、getWorkflowExecutionMetadata。用于提供执行通用工具能力（…
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Core execution engine -> application/services/execution_engine
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/execution-engine/node-execution-context/utils/execution-metadata.ts -> services/n8n/application/core/services/execution_engine/node-execution-context/utils/execution_metadata.py

import type { IRunExecutionData } from 'n8n-workflow';
import { LoggerProxy as Logger } from 'n8n-workflow';

import { InvalidExecutionMetadataError } from '@/errors/invalid-execution-metadata.error';

export const KV_LIMIT = 10;

export function setWorkflowExecutionMetadata(
	executionData: IRunExecutionData,
	key: string,
	value: unknown,
) {
	if (!executionData.resultData.metadata) {
		executionData.resultData.metadata = {};
	}
	// Currently limited to 10 metadata KVs
	if (
		!(key in executionData.resultData.metadata) &&
		Object.keys(executionData.resultData.metadata).length >= KV_LIMIT
	) {
		return;
	}
	if (typeof key !== 'string') {
		throw new InvalidExecutionMetadataError('key', key);
	}
	if (key.replace(/[A-Za-z0-9_]/g, '').length !== 0) {
		throw new InvalidExecutionMetadataError(
			'key',
			key,
			`Custom date key can only contain characters "A-Za-z0-9_" (key "${key}")`,
		);
	}
	if (typeof value !== 'string' && typeof value !== 'number' && typeof value !== 'bigint') {
		throw new InvalidExecutionMetadataError('value', key);
	}
	const val = String(value);
	if (key.length > 50) {
		Logger.error('Custom data key over 50 characters long. Truncating to 50 characters.');
	}
	if (val.length > 255) {
		Logger.error('Custom data value over 512 characters long. Truncating to 512 characters.');
	}
	executionData.resultData.metadata[key.slice(0, 50)] = val.slice(0, 512);
}

export function setAllWorkflowExecutionMetadata(
	executionData: IRunExecutionData,
	obj: Record<string, string>,
) {
	const errors: Error[] = [];
	Object.entries(obj).forEach(([key, value]) => {
		try {
			setWorkflowExecutionMetadata(executionData, key, value);
		} catch (e) {
			errors.push(e as Error);
		}
	});
	if (errors.length) {
		throw errors[0];
	}
}

export function getAllWorkflowExecutionMetadata(
	executionData: IRunExecutionData,
): Record<string, string> {
	// Make a copy so it can't be modified directly
	return executionData.resultData.metadata ? { ...executionData.resultData.metadata } : {};
}

export function getWorkflowExecutionMetadata(
	executionData: IRunExecutionData,
	key: string,
): string {
	return getAllWorkflowExecutionMetadata(executionData)[String(key).slice(0, 50)];
}
