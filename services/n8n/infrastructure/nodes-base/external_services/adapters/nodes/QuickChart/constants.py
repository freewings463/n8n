"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/QuickChart/constants.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/QuickChart 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:CHART_TYPE_OPTIONS、HORIZONTAL_CHARTS、ITEM_STYLE_CHARTS、Fill_CHARTS、POINT_STYLE_CHARTS。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/QuickChart/constants.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/QuickChart/constants.py

import type { INodePropertyOptions } from 'n8n-workflow';

// Disable some charts that use different datasets for now
export const CHART_TYPE_OPTIONS: INodePropertyOptions[] = [
	{
		name: 'Bar Chart',
		value: 'bar',
	},
	{
		name: 'Doughnut Chart',
		value: 'doughnut',
	},
	{
		name: 'Line Chart',
		value: 'line',
	},
	{
		name: 'Pie Chart',
		value: 'pie',
	},
	{
		name: 'Polar Chart',
		value: 'polarArea',
	},
];

export const HORIZONTAL_CHARTS = ['bar', 'boxplot', 'violin'];
export const ITEM_STYLE_CHARTS = ['boxplot', 'horizontalBoxplot', 'violin', 'horizontalViolin'];
export const Fill_CHARTS = ['line'];
export const POINT_STYLE_CHARTS = ['line'];
