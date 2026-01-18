"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SeaTable/v1/Interfaces.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SeaTable/v1 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:IApi、IServerInfo、IAppAccessToken、IDtableMetadataColumn、TDtableViewColumn、IDtableMetadataTable、IDtableMetadata、IEndpointVariables 等6项。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SeaTable/v1/Interfaces.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SeaTable/v1/Interfaces.py

import type {
	TColumnType,
	TColumnValue,
	TDtableMetadataColumns,
	TDtableMetadataTables,
	TSeaTableServerEdition,
	TSeaTableServerVersion,
} from './types';

export interface IApi {
	server: string;
	token: string;
	appAccessToken?: IAppAccessToken;
	info?: IServerInfo;
}

export interface IServerInfo {
	version: TSeaTableServerVersion;
	edition: TSeaTableServerEdition;
}

export interface IAppAccessToken {
	app_name: string;
	access_token: string;
	dtable_uuid: string;
	dtable_server: string;
	dtable_socket: string;
	workspace_id: number;
	dtable_name: string;
}

export interface IDtableMetadataColumn {
	key: string;
	name: string;
	type: TColumnType;
	editable: boolean;
}

export interface TDtableViewColumn {
	_id: string;
	name: string;
}

export interface IDtableMetadataTable {
	_id: string;
	name: string;
	columns: TDtableMetadataColumns;
}

export interface IDtableMetadata {
	tables: TDtableMetadataTables;
	version: string;
	format_version: string;
}

export interface IEndpointVariables {
	[name: string]: string | undefined;
}

export interface IRowObject {
	[name: string]: TColumnValue;
}

export interface IRow extends IRowObject {
	_id: string;
	_ctime: string;
	_mtime: string;
	_seq?: number;
}

export interface IName {
	name: string;
}

type TOperation = 'cloudHosted' | 'selfHosted';

export interface ICredential {
	token: string;
	domain: string;
	environment: TOperation;
}

interface IBase {
	dtable_uuid: string;
	access_token: string;
}

export interface ICtx {
	base?: IBase;
	credentials?: ICredential;
}

export interface IRowResponse {
	metadata: [
		{
			key: string;
			name: string;
		},
	];
	results: IRow[];
}
