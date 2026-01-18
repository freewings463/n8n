"""
MIGRATION-META:
  source_path: packages/cli/src/modules/source-control.ee/types/exportable-workflow.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/source-control.ee/types 的工作流类型。导入/依赖:外部:无；内部:n8n-workflow；本地:./resource-owner。导出:ExportableWorkflow。关键函数/方法:无。用于定义工作流相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/source-control.ee/types/exportable-workflow.ts -> services/n8n/application/cli/services/modules/source-control.ee/types/exportable_workflow.py

import type { INode, IConnections, IWorkflowSettings } from 'n8n-workflow';

import type { RemoteResourceOwner } from './resource-owner';

export interface ExportableWorkflow {
	id: string;
	name: string;
	nodes: INode[];
	connections: IConnections;
	settings?: IWorkflowSettings;
	triggerCount: number;
	versionId?: string;
	owner: RemoteResourceOwner;
	parentFolderId: string | null;
	isArchived: boolean;
}
