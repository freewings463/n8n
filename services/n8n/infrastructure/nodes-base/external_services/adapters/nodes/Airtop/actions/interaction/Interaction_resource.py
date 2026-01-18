"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtop/actions/interaction/Interaction.resource.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtop/actions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./click.operation、./fill.operation、./hover.operation、./scroll.operation 等2项。导出:click、fill、hover、scroll、type、description。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtop/actions/interaction/Interaction.resource.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtop/actions/interaction/Interaction_resource.py

import type { INodeProperties } from 'n8n-workflow';

import * as click from './click.operation';
import * as fill from './fill.operation';
import * as hover from './hover.operation';
import * as scroll from './scroll.operation';
import * as type from './type.operation';
import { sessionIdField, windowIdField } from '../common/fields';
export { click, fill, hover, scroll, type };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['interaction'],
			},
		},
		options: [
			{
				name: 'Click an Element',
				value: 'click',
				description: 'Execute a click on an element given a description',
				action: 'Click an element',
			},
			{
				name: 'Fill Form',
				value: 'fill',
				description: 'Fill a form with the provided information',
				action: 'Fill form',
			},
			{
				name: 'Hover on an Element',
				value: 'hover',
				description: 'Execute a hover action on an element given a description',
				action: 'Hover on an element',
			},
			{
				name: 'Scroll',
				value: 'scroll',
				description: 'Execute a scroll action on the page',
				action: 'Scroll on page',
			},
			{
				name: 'Type',
				value: 'type',
				description: 'Execute a Type action on an element given a description',
				action: 'Type text',
			},
		],
		default: 'click',
	},
	{
		...sessionIdField,
		displayOptions: {
			show: {
				resource: ['interaction'],
			},
		},
	},
	{
		...windowIdField,
		displayOptions: {
			show: {
				resource: ['interaction'],
			},
		},
	},
	...click.description,
	...fill.description,
	...hover.description,
	...scroll.description,
	...type.description,
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['interaction'],
				operation: ['click', 'hover', 'type', 'scroll'],
			},
		},
		options: [
			{
				displayName: 'Visual Scope',
				name: 'visualScope',
				type: 'options',
				default: 'auto',
				description: 'Defines the strategy for visual analysis of the current window',
				options: [
					{
						name: 'Auto',
						description: 'Provides the simplest out-of-the-box experience for most web pages',
						value: 'auto',
					},
					{
						name: 'Viewport',
						description: 'For analysis of the current browser view only',
						value: 'viewport',
					},
					{
						name: 'Page',
						description: 'For analysis of the entire page',
						value: 'page',
					},
					{
						name: 'Scan',
						description:
							"For a full page analysis on sites that have compatibility issues with 'Page' mode",
						value: 'scan',
					},
				],
			},
			{
				displayName: 'Wait Until Event After Navigation',
				name: 'waitForNavigation',
				type: 'options',
				default: 'load',
				description:
					"The condition to wait for the navigation to complete after an interaction (click, type or hover). Defaults to 'Fully Loaded'.",
				options: [
					{
						name: 'Fully Loaded (Slower)',
						value: 'load',
					},
					{
						name: 'DOM Only Loaded (Faster)',
						value: 'domcontentloaded',
					},
					{
						name: 'All Network Activity Has Stopped',
						value: 'networkidle0',
					},
					{
						name: 'Most Network Activity Has Stopped',
						value: 'networkidle2',
					},
				],
			},
		],
	},
];
