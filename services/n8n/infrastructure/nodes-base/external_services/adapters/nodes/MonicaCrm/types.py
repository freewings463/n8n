"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/MonicaCrm/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/MonicaCrm 的类型。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:LoaderGetResponse、Option。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/MonicaCrm/types.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/MonicaCrm/types.py

import type { IDataObject } from 'n8n-workflow';

export type LoaderGetResponse = {
	data: Array<{
		id: string;
		name: string;
	}>;
} & IDataObject;

export type Option = {
	value: string;
	name: string;
};
