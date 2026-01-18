"""
MIGRATION-META:
  source_path: packages/@n8n/benchmark/src/n8n-api-client/n8n-api-client.types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/benchmark/src/n8n-api-client 的类型。导入/依赖:外部:无；内部:无；本地:无。导出:Workflow、Credential、DataTableColumn、DataTable。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。注释目标:n8n workflow. This is a simplified version of the actual workflow object.。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Benchmark n8n API client -> infrastructure/external_services/clients
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/benchmark/src/n8n-api-client/n8n-api-client.types.ts -> services/n8n/infrastructure/n8n-benchmark/external_services/clients/n8n_api_client/n8n_api_client_types.py

/**
 * n8n workflow. This is a simplified version of the actual workflow object.
 */
export type Workflow = {
	id: string;
	name: string;
	versionId: string;
	tags?: string[];
};

export type Credential = {
	id: string;
	name: string;
	type: string;
};

export type DataTableColumn = {
	name: string;
	type: 'string' | 'number' | 'boolean' | 'date';
};

export type DataTable = {
	id?: string;
	projectId?: number;
	name: string;
	columns: DataTableColumn[];
};
