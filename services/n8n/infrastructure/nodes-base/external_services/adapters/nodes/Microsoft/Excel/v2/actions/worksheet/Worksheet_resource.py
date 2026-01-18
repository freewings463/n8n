"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Excel/v2/actions/worksheet/Worksheet.resource.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Excel 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./append.operation、./clear.operation、./deleteWorksheet.operation、./getAll.operation 等3项。导出:append、clear、deleteWorksheet、getAll、readRows、update、upsert、description。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Excel/v2/actions/worksheet/Worksheet.resource.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Excel/v2/actions/worksheet/Worksheet_resource.py

import type { INodeProperties } from 'n8n-workflow';

import * as append from './append.operation';
import * as clear from './clear.operation';
import * as deleteWorksheet from './deleteWorksheet.operation';
import * as getAll from './getAll.operation';
import * as readRows from './readRows.operation';
import * as update from './update.operation';
import * as upsert from './upsert.operation';

export { append, clear, deleteWorksheet, getAll, readRows, update, upsert };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['worksheet'],
			},
		},
		options: [
			{
				name: 'Append',
				value: 'append',
				description: 'Append data to sheet',
				action: 'Append data to sheet',
			},
			{
				// eslint-disable-next-line n8n-nodes-base/node-param-option-name-wrong-for-upsert
				name: 'Append or Update',
				value: 'upsert',
				// eslint-disable-next-line n8n-nodes-base/node-param-description-wrong-for-upsert
				description: 'Append a new row or update the current one if it already exists (upsert)',
				action: 'Append or update a sheet',
			},
			{
				name: 'Clear',
				value: 'clear',
				description: 'Clear sheet',
				action: 'Clear sheet',
			},
			{
				name: 'Delete',
				value: 'deleteWorksheet',
				description: 'Delete sheet',
				action: 'Delete sheet',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get a list of sheets',
				action: 'Get sheets',
			},
			{
				name: 'Get Rows',
				value: 'readRows',
				description: 'Retrieve a list of sheet rows',
				action: 'Get rows from sheet',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update rows of a sheet or sheet range',
				action: 'Update sheet',
			},
		],
		default: 'getAll',
	},
	...append.description,
	...clear.description,
	...deleteWorksheet.description,
	...getAll.description,
	...readRows.description,
	...update.description,
	...upsert.description,
];
