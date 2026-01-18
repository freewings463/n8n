"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SeaTable/v2/Schema.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SeaTable/v2 的节点。导入/依赖:外部:无；内部:无；本地:./types。导出:ColumnType、schema。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SeaTable/v2/Schema.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SeaTable/v2/Schema.py

import type { TColumnType, TDateTimeFormat, TInheritColumnKey } from './types';

export type ColumnType = keyof typeof schema.columnTypes;

export const schema = {
	rowFetchSegmentLimit: 1000,
	dateTimeFormat: 'YYYY-MM-DDTHH:mm:ss.SSSZ',
	internalNames: {
		_id: 'text',
		_creator: 'creator',
		_ctime: 'ctime',
		_last_modifier: 'last-modifier',
		_mtime: 'mtime',
		_seq: 'auto-number',
	},
	columnTypes: {
		text: 'Text',
		'long-text': 'Long Text',
		number: 'Number',
		collaborator: 'Collaborator',
		date: 'Date',
		duration: 'Duration',
		'single-select': 'Single Select',
		'multiple-select': 'Multiple Select',
		image: 'Image',
		file: 'File',
		email: 'Email',
		url: 'URL',
		checkbox: 'Checkbox',
		rate: 'Rating',
		formula: 'Formula',
		'link-formula': 'Link-Formula',
		geolocation: 'Geolocation',
		link: 'Link',
		creator: 'Creator',
		ctime: 'Created time',
		'last-modifier': 'Last Modifier',
		mtime: 'Last modified time',
		'auto-number': 'Auto number',
		button: 'Button',
		'digital-sign': 'Digital Signature',
	},
	nonUpdateAbleColumnTypes: {
		creator: 'creator',
		ctime: 'ctime',
		'last-modifier': 'last-modifier',
		mtime: 'mtime',
		'auto-number': 'auto-number',
		button: 'button',
		formula: 'formula',
		'link-formula': 'link-formula',
		link: 'link',
		'digital-sign': 'digital-sign',
	},
} as {
	rowFetchSegmentLimit: number;
	dateTimeFormat: TDateTimeFormat;
	internalNames: { [key in TInheritColumnKey]: ColumnType };
	columnTypes: { [key in TColumnType]: string };
	nonUpdateAbleColumnTypes: { [key in ColumnType]: ColumnType };
};
