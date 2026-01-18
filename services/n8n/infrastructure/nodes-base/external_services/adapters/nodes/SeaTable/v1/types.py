"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SeaTable/v1/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SeaTable/v1 的类型。导入/依赖:外部:无；内部:n8n-workflow；本地:./Interfaces。导出:TSeaTableServerVersion、TSeaTableServerEdition、TInheritColumnTypeTime、TInheritColumnTypeUser、TColumnType、TInheritColumnKey、TColumnValue、TColumnKey 等13项。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。注释目标:---------------------------------- / sea-table。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SeaTable/v1/types.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SeaTable/v1/types.py

// ----------------------------------
//         sea-table
// ----------------------------------

export type TSeaTableServerVersion = '2.0.6';
export type TSeaTableServerEdition = 'enterprise edition';

// ----------------------------------
//         dtable
// ----------------------------------

import type { ICredentialDataDecryptedObject } from 'n8n-workflow';

import type { IDtableMetadataColumn, IDtableMetadataTable, TDtableViewColumn } from './Interfaces';

export type TInheritColumnTypeTime = 'ctime' | 'mtime';
export type TInheritColumnTypeUser = 'creator' | 'last-modifier';
export type TColumnType =
	| 'text'
	| 'long-text'
	| 'number'
	| 'collaborator'
	| 'date'
	| 'duration'
	| 'single-select'
	| 'multiple-select'
	| 'email'
	| 'url'
	| 'rate'
	| 'checkbox'
	| 'formula'
	| TInheritColumnTypeTime
	| TInheritColumnTypeUser
	| 'auto-number';

type TImplementInheritColumnKey = '_seq';
export type TInheritColumnKey =
	| '_id'
	| '_creator'
	| '_ctime'
	| '_last_modifier'
	| '_mtime'
	| TImplementInheritColumnKey;

export type TColumnValue = undefined | boolean | number | string | string[] | null;
export type TColumnKey = TInheritColumnKey | string;

export type TDtableMetadataTables = readonly IDtableMetadataTable[];
export type TDtableMetadataColumns = readonly IDtableMetadataColumn[];
export type TDtableViewColumns = readonly TDtableViewColumn[];

// ----------------------------------
//         api
// ----------------------------------

export type TEndpointVariableName = 'access_token' | 'dtable_uuid' | 'server';

// Template Literal Types requires-ts-4.1.5 -- deferred
export type TMethod = 'GET' | 'POST';
type TEndpoint =
	| '/api/v2.1/dtable/app-access-token/'
	| '/dtable-server/api/v1/dtables/{{dtable_uuid}}/rows/';
export type TEndpointExpr = TEndpoint;
export type TEndpointResolvedExpr =
	TEndpoint; /* deferred: but already in use for header values, e.g. authentication */

export type TDateTimeFormat = 'YYYY-MM-DDTHH:mm:ss.SSSZ' /* moment.js */;

// ----------------------------------
//         node
// ----------------------------------

export type TCredentials = ICredentialDataDecryptedObject | undefined;

export type TTriggerOperation = 'create' | 'update';

export type TOperation = 'append' | 'list' | 'metadata';

export type TLoadedResource = {
	name: string;
};
export type TColumnsUiValues = Array<{
	columnName: string;
	columnValue: string;
}>;
