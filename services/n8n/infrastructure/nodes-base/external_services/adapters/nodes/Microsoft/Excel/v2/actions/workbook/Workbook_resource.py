"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Excel/v2/actions/workbook/Workbook.resource.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Excel 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./addWorksheet.operation、./deleteWorkbook.operation、./getAll.operation。导出:addWorksheet、deleteWorkbook、getAll、description。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Excel/v2/actions/workbook/Workbook.resource.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Excel/v2/actions/workbook/Workbook_resource.py

import type { INodeProperties } from 'n8n-workflow';

import * as addWorksheet from './addWorksheet.operation';
import * as deleteWorkbook from './deleteWorkbook.operation';
import * as getAll from './getAll.operation';

export { addWorksheet, deleteWorkbook, getAll };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['workbook'],
			},
		},
		options: [
			{
				name: 'Add Sheet',
				value: 'addWorksheet',
				description: 'Add a new sheet to the workbook',
				action: 'Add a sheet to a workbook',
			},
			{
				name: 'Delete',
				value: 'deleteWorkbook',
				description: 'Delete workbook',
				action: 'Delete workbook',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get workbooks',
				action: 'Get workbooks',
			},
		],
		default: 'getAll',
	},
	...addWorksheet.description,
	...deleteWorkbook.description,
	...getAll.description,
];
