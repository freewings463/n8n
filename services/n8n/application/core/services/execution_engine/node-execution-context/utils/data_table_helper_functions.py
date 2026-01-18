"""
MIGRATION-META:
  source_path: packages/core/src/execution-engine/node-execution-context/utils/data-table-helper-functions.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/execution-engine/node-execution-context/utils 的执行工具。导入/依赖:外部:无；内部:无；本地:无。导出:getDataTableHelperFunctions。关键函数/方法:getDataTableHelperFunctions。用于提供执行通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Core execution engine -> application/services/execution_engine
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/execution-engine/node-execution-context/utils/data-table-helper-functions.ts -> services/n8n/application/core/services/execution_engine/node-execution-context/utils/data_table_helper_functions.py

import type {
	DataTableProxyFunctions,
	INode,
	Workflow,
	IWorkflowExecuteAdditionalData,
} from 'n8n-workflow';

export function getDataTableHelperFunctions(
	additionalData: IWorkflowExecuteAdditionalData,
	workflow: Workflow,
	node: INode,
): Partial<DataTableProxyFunctions> {
	const dataTableProxyProvider = additionalData['data-table']?.dataTableProxyProvider;
	if (!dataTableProxyProvider) return {};
	return {
		getDataTableAggregateProxy: async () =>
			await dataTableProxyProvider.getDataTableAggregateProxy(
				workflow,
				node,
				additionalData.dataTableProjectId,
			),
		getDataTableProxy: async (dataTableId: string) =>
			await dataTableProxyProvider.getDataTableProxy(
				workflow,
				node,
				dataTableId,
				additionalData.dataTableProjectId,
			),
	};
}
