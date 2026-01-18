"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/BigQuery/v2/helpers/interfaces.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/BigQuery 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:SchemaField、TableSchema、TableRawData、JobReference、ResponseWithJobReference。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/BigQuery/v2/helpers/interfaces.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/BigQuery/v2/helpers/interfaces.py

import type { IDataObject } from 'n8n-workflow';

export type SchemaField = {
	name: string;
	type: string;
	mode: string;
	fields?: SchemaField[];
};

export type TableSchema = {
	fields: SchemaField[];
};

export type TableRawData = {
	f: Array<{ v: IDataObject | TableRawData }>;
};

export type JobReference = {
	projectId: string;
	jobId: string;
	location: string;
};

export type ResponseWithJobReference = {
	kind: string;
	id: string;
	jobReference: JobReference;
	status: {
		state: 'PENDING' | 'RUNNING' | 'DONE';
	};
};
