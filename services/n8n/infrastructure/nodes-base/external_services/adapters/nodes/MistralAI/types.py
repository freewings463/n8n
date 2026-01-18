"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/MistralAI/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/MistralAI 的类型。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:BatchJob、BatchItemResult、Page。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/MistralAI/types.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/MistralAI/types.py

import type { IDataObject } from 'n8n-workflow';

export interface BatchJob {
	id: string;
	status:
		| 'QUEUED'
		| 'RUNNING'
		| 'SUCCESS'
		| 'FAILED'
		| 'TIMEOUT_EXCEEDED'
		| 'CANCELLATION_REQUESTED'
		| 'CANCELLED';
	output_file: string;
	errors: IDataObject[];
}

export interface BatchItemResult {
	id: string;
	custom_id: string;
	response: {
		body: {
			pages: Page[];
		};
	};
	error?: IDataObject;
}

export interface Page {
	index: number;
	markdown: string;
	images: IDataObject[];
}
