"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/SharePoint/helpers/interfaces.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/SharePoint 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:IListColumnType、IDriveItem、IListItem、IList、ISite、IErrorResponse。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/SharePoint/helpers/interfaces.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/SharePoint/helpers/interfaces.py

import type { IDataObject } from 'n8n-workflow';

export interface IListColumnType {
	id: string;
	hidden: boolean;
	name: string;
	displayName: string;
	readOnly: boolean;
	required: boolean;
	type: string;
	enforceUniqueValues: boolean;
	choice?: {
		choices: string[];
	};
}

export interface IDriveItem {
	id: string;
	name: string;
	file?: IDataObject;
	folder?: IDataObject;
}

export interface IListItem {
	id: string;
	fields: {
		Title: string;
	};
}

export interface IList {
	id: string;
	displayName: string;
}

export interface ISite {
	id: string;
	title: string;
}

export interface IErrorResponse {
	error: {
		code: string;
		message: string;
	};
}
