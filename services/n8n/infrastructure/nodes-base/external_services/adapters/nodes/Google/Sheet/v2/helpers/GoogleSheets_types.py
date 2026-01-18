"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Sheet/v2/helpers/GoogleSheets.types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Sheet 的类型。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:ROW_NUMBER、ISheetOptions、IGoogleAuthCredentials、ISheetUpdateData、ILookupValues、IToDeleteRange、IToDelete、ValueInputOption 等14项。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Sheet/v2/helpers/GoogleSheets.types.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Sheet/v2/helpers/GoogleSheets_types.py

import type { AllEntities, Entity, PropertiesOf } from 'n8n-workflow';

export const ROW_NUMBER = 'row_number';

export interface ISheetOptions {
	scope: string[];
}

export interface IGoogleAuthCredentials {
	email: string;
	privateKey: string;
}

export interface ISheetUpdateData {
	range: string;
	values: string[][];
}

export interface ILookupValues {
	lookupColumn: string;
	lookupValue: string;
}

export interface IToDeleteRange {
	amount: number;
	startIndex: number;
	sheetId: number;
}

export interface IToDelete {
	[key: string]: IToDeleteRange[] | undefined;
	columns?: IToDeleteRange[];
	rows?: IToDeleteRange[];
}

export type ValueInputOption = 'RAW' | 'USER_ENTERED';

export type ValueRenderOption = 'FORMATTED_VALUE' | 'FORMULA' | 'UNFORMATTED_VALUE';

export type RangeDetectionOptions = {
	rangeDefinition: 'detectAutomatically' | 'specifyRange' | 'specifyRangeA1';
	readRowsUntil?: 'firstEmptyRow' | 'lastRowInSheet';
	headerRow?: string;
	firstDataRow?: string;
	range?: string;
};

export type SheetDataRow = Array<string | number>;
export type SheetRangeData = SheetDataRow[];

// delete is del
type GoogleSheetsMap = {
	spreadsheet: 'create' | 'deleteSpreadsheet';
	sheet: 'append' | 'clear' | 'create' | 'delete' | 'read' | 'remove' | 'update' | 'appendOrUpdate';
};

export type GoogleSheets = AllEntities<GoogleSheetsMap>;

export type GoogleSheetsSpreadSheet = Entity<GoogleSheetsMap, 'spreadsheet'>;
export type GoogleSheetsSheet = Entity<GoogleSheetsMap, 'sheet'>;

export type SpreadSheetProperties = PropertiesOf<GoogleSheetsSpreadSheet>;
export type SheetProperties = PropertiesOf<GoogleSheetsSheet>;

export type ResourceLocator = 'id' | 'url' | 'list' | 'name';

export const ResourceLocatorUiNames = {
	id: 'By ID',
	url: 'By URL',
	list: 'From List',
	name: 'By Name',
};

type SpreadSheetResponseSheet = {
	properties: {
		title: string;
		sheetId: number;
	};
};

export type SpreadSheetResponse = {
	sheets: SpreadSheetResponseSheet[];
};

export type SheetCellDecoded = {
	cell?: string;
	column?: string;
	row?: number;
};

export type SheetRangeDecoded = {
	nameWithRange: string;
	name: string;
	range: string;
	start?: SheetCellDecoded;
	end?: SheetCellDecoded;
};
