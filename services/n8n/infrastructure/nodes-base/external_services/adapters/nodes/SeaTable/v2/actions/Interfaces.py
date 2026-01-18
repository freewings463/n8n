"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SeaTable/v2/actions/Interfaces.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SeaTable/v2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:SeaTable、SeaTableRow、SeaTableBase、SeaTableLink、SeaTableAsset、RowProperties、BaseProperties、LinkProperties 等25项。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SeaTable/v2/actions/Interfaces.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SeaTable/v2/actions/Interfaces.py

import type { AllEntities, Entity, PropertiesOf } from 'n8n-workflow';

type SeaTableMap = {
	row: 'create' | 'get' | 'search' | 'update' | 'remove' | 'lock' | 'unlock' | 'list';
	base: 'snapshot' | 'metadata' | 'collaborator';
	link: 'add' | 'list' | 'remove';
	asset: 'upload' | 'getPublicURL';
};

export type SeaTable = AllEntities<SeaTableMap>;

export type SeaTableRow = Entity<SeaTableMap, 'row'>;
export type SeaTableBase = Entity<SeaTableMap, 'base'>;
export type SeaTableLink = Entity<SeaTableMap, 'link'>;
export type SeaTableAsset = Entity<SeaTableMap, 'asset'>;

export type RowProperties = PropertiesOf<SeaTableRow>;
export type BaseProperties = PropertiesOf<SeaTableBase>;
export type LinkProperties = PropertiesOf<SeaTableLink>;
export type AssetProperties = PropertiesOf<SeaTableAsset>;

import type {
	TColumnType,
	TColumnValue,
	TDtableMetadataColumns,
	TDtableMetadataTables,
	TSeaTableServerEdition,
	TSeaTableServerVersion,
} from '../types';

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
	editable?: boolean;
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
	[name: string]: string | number | undefined;
}

export interface IRowObject {
	[name: string]: TColumnValue | object;
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
	workspace_id: number;
	dtable_name: string;
}

export interface ICtx {
	base?: IBase;
	credentials?: ICredential;
}

// response object of SQL-Query!
export interface IRowResponse {
	metadata: [
		{
			key: string;
			name: string;
			type: string;
		},
	];
	results: IRow[];
}

// das ist bad
export interface IRowResponse2 {
	rows: IRow[];
}

/** neu von mir **/

// response object of SQL-Query!
export interface ISqlQueryResult {
	metadata: [
		{
			key: string;
			name: string;
		},
	];
	results: IRow[];
}

// response object of GetMetadata
export interface IGetMetadataResult {
	metadata: IDtableMetadata;
}

// response object of GetRows
export interface IGetRowsResult {
	rows: IRow[];
}

export interface ICollaboratorsResult {
	user_list: ICollaborator[];
}

export interface ICollaborator {
	email: string;
	name: string;
	contact_email: string;
	avatar_url?: string;
	id_in_org?: string;
}

export interface IColumnDigitalSignature {
	username: string;
	sign_image_url: string;
	sign_time: string;
	contact_email?: string;
	name: string;
}

export interface IFile {
	name: string;
	size: number;
	type: 'file';
	url: string;
	path?: string;
}

export interface ILinkData {
	table_id: string;
	other_table_id: string;
	link_id: string;
}

export interface IUploadLink {
	upload_link: string;
	parent_path: string;
	img_relative_path: string;
	file_relative_path: string;
}
