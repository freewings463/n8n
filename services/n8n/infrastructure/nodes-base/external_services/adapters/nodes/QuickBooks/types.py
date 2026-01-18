"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/QuickBooks/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/QuickBooks 的类型。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:QuickBooksOAuth2Credentials、DateFieldsUi、TransactionFields、Option、TransactionReport。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/QuickBooks/types.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/QuickBooks/types.py

import type { IDataObject } from 'n8n-workflow';

export type QuickBooksOAuth2Credentials = {
	environment: 'production' | 'sandbox';
	oauthTokenData: {
		callbackQueryString: {
			realmId: string;
		};
	};
};

export type DateFieldsUi = Partial<{
	dateRangeCustom: DateFieldUi;
	dateRangeDueCustom: DateFieldUi;
	dateRangeModificationCustom: DateFieldUi;
	dateRangeCreationCustom: DateFieldUi;
}>;

type DateFieldUi = {
	[key: string]: {
		[key: string]: string;
	};
};

export type TransactionFields = Partial<{
	columns: string[];
	memo: string[];
	term: string[];
	customer: string[];
	vendor: string[];
}> &
	DateFieldsUi &
	IDataObject;

export type Option = { name: string; value: string };

export type TransactionReport = {
	Columns: {
		Column: Array<{
			ColTitle: string;
			ColType: string;
		}>;
	};
	Rows: {
		Row: Array<{
			ColData: Array<{ value: string }>;
		}>;
	};
};
