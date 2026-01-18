"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtop/actions/window/Window.resource.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtop/actions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./close.operation、./create.operation、./getLiveView.operation、./list.operation 等3项。导出:create、close、takeScreenshot、load、list、getLiveView、description。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtop/actions/window/Window.resource.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtop/actions/window/Window_resource.py

import type { INodeProperties } from 'n8n-workflow';

import * as close from './close.operation';
import * as create from './create.operation';
import * as getLiveView from './getLiveView.operation';
import * as list from './list.operation';
import * as load from './load.operation';
import * as takeScreenshot from './takeScreenshot.operation';
import { sessionIdField, windowIdField } from '../common/fields';

export { create, close, takeScreenshot, load, list, getLiveView };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		typeOptions: {
			sortable: false,
		},
		displayOptions: {
			show: {
				resource: ['window'],
			},
		},
		options: [
			{
				name: 'Close Window',
				value: 'close',
				description: 'Close a window inside a session',
				action: 'Close a window',
			},
			{
				name: 'Create a New Browser Window',
				value: 'create',
				description: 'Create a new browser window inside a session. Can load a URL when created.',
				action: 'Create a window',
			},
			{
				name: 'Get Live View',
				value: 'getLiveView',
				description: 'Get information about a browser window, including the live view URL',
				action: 'Get live view',
			},
			{
				name: 'List Windows',
				value: 'list',
				description: 'List all browser windows in a session',
				action: 'List windows',
			},
			{
				name: 'Load URL',
				value: 'load',
				description: 'Load a URL in an existing window',
				action: 'Load a page',
			},
			{
				name: 'Take Screenshot',
				value: 'takeScreenshot',
				description: 'Take a screenshot of the current window',
				action: 'Take screenshot',
			},
		],
		default: 'create',
	},
	{
		...sessionIdField,
		displayOptions: {
			show: {
				resource: ['window'],
			},
		},
	},
	{
		...windowIdField,
		displayOptions: {
			show: {
				resource: ['window'],
				operation: ['close', 'takeScreenshot', 'load', 'getLiveView'],
			},
		},
	},
	...create.description,
	...list.description,
	...getLiveView.description,
	...load.description,
	...takeScreenshot.description,
];
