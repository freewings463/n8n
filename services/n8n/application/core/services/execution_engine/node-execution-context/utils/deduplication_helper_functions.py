"""
MIGRATION-META:
  source_path: packages/core/src/execution-engine/node-execution-context/utils/deduplication-helper-functions.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/execution-engine/node-execution-context/utils 的执行工具。导入/依赖:外部:无；内部:@/data-deduplication-service；本地:无。导出:getDeduplicationHelperFunctions。关键函数/方法:checkProcessedAndRecord、checkProcessedItemsAndRecord、removeProcessed、clearAllProcessedItems、getProcessedDataCount、getDeduplicationHelperFunctions。用于提供执行通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Core execution engine -> application/services/execution_engine
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/execution-engine/node-execution-context/utils/deduplication-helper-functions.ts -> services/n8n/application/core/services/execution_engine/node-execution-context/utils/deduplication_helper_functions.py

import type {
	IDataObject,
	INode,
	Workflow,
	DeduplicationHelperFunctions,
	IDeduplicationOutput,
	IDeduplicationOutputItems,
	ICheckProcessedOptions,
	DeduplicationScope,
	DeduplicationItemTypes,
	ICheckProcessedContextData,
} from 'n8n-workflow';

import { DataDeduplicationService } from '@/data-deduplication-service';

async function checkProcessedAndRecord(
	items: DeduplicationItemTypes[],
	scope: DeduplicationScope,
	contextData: ICheckProcessedContextData,
	options: ICheckProcessedOptions,
): Promise<IDeduplicationOutput> {
	return await DataDeduplicationService.getInstance().checkProcessedAndRecord(
		items,
		scope,
		contextData,
		options,
	);
}

async function checkProcessedItemsAndRecord(
	key: string,
	items: IDataObject[],
	scope: DeduplicationScope,
	contextData: ICheckProcessedContextData,
	options: ICheckProcessedOptions,
): Promise<IDeduplicationOutputItems> {
	return await DataDeduplicationService.getInstance().checkProcessedItemsAndRecord(
		key,
		items,
		scope,
		contextData,
		options,
	);
}

async function removeProcessed(
	items: DeduplicationItemTypes[],
	scope: DeduplicationScope,
	contextData: ICheckProcessedContextData,
	options: ICheckProcessedOptions,
): Promise<void> {
	return await DataDeduplicationService.getInstance().removeProcessed(
		items,
		scope,
		contextData,
		options,
	);
}

async function clearAllProcessedItems(
	scope: DeduplicationScope,
	contextData: ICheckProcessedContextData,
	options: ICheckProcessedOptions,
): Promise<void> {
	return await DataDeduplicationService.getInstance().clearAllProcessedItems(
		scope,
		contextData,
		options,
	);
}

async function getProcessedDataCount(
	scope: DeduplicationScope,
	contextData: ICheckProcessedContextData,
	options: ICheckProcessedOptions,
): Promise<number> {
	return await DataDeduplicationService.getInstance().getProcessedDataCount(
		scope,
		contextData,
		options,
	);
}

export const getDeduplicationHelperFunctions = (
	workflow: Workflow,
	node: INode,
): DeduplicationHelperFunctions => ({
	async checkProcessedAndRecord(
		items: DeduplicationItemTypes[],
		scope: DeduplicationScope,
		options: ICheckProcessedOptions,
	): Promise<IDeduplicationOutput> {
		return await checkProcessedAndRecord(items, scope, { node, workflow }, options);
	},
	async checkProcessedItemsAndRecord(
		propertyName: string,
		items: IDataObject[],
		scope: DeduplicationScope,
		options: ICheckProcessedOptions,
	): Promise<IDeduplicationOutputItems> {
		return await checkProcessedItemsAndRecord(
			propertyName,
			items,
			scope,
			{ node, workflow },
			options,
		);
	},
	async removeProcessed(
		items: DeduplicationItemTypes[],
		scope: DeduplicationScope,
		options: ICheckProcessedOptions,
	): Promise<void> {
		return await removeProcessed(items, scope, { node, workflow }, options);
	},
	async clearAllProcessedItems(
		scope: DeduplicationScope,
		options: ICheckProcessedOptions,
	): Promise<void> {
		return await clearAllProcessedItems(scope, { node, workflow }, options);
	},
	async getProcessedDataCount(
		scope: DeduplicationScope,
		options: ICheckProcessedOptions,
	): Promise<number> {
		return await getProcessedDataCount(scope, { node, workflow }, options);
	},
});
