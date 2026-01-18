"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Code/descriptions/JavascriptCodeDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Code/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:javascriptCodeDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Code/descriptions/JavascriptCodeDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Code/descriptions/JavascriptCodeDescription.py

import type { INodeProperties } from 'n8n-workflow';

const commonDescription: INodeProperties = {
	displayName: 'JavaScript',
	name: 'jsCode',
	type: 'string',
	typeOptions: {
		editor: 'codeNodeEditor',
		editorLanguage: 'javaScript',
	},
	default: '',
	description:
		'JavaScript code to execute.<br><br>Tip: You can use luxon vars like <code>$today</code> for dates and <code>$jmespath</code> for querying JSON structures. <a href="https://docs.n8n.io/nodes/n8n-nodes-base.function">Learn more</a>.',
	noDataExpression: true,
};

const v1Properties: INodeProperties[] = [
	{
		...commonDescription,
		displayOptions: {
			show: {
				'@version': [1],
				mode: ['runOnceForAllItems'],
			},
		},
	},
	{
		...commonDescription,
		displayOptions: {
			show: {
				'@version': [1],
				mode: ['runOnceForEachItem'],
			},
		},
	},
];

const v2Properties: INodeProperties[] = [
	{
		...commonDescription,
		displayOptions: {
			show: {
				'@version': [2],
				language: ['javaScript'],
				mode: ['runOnceForAllItems'],
			},
		},
	},
	{
		...commonDescription,
		displayOptions: {
			show: {
				'@version': [2],
				language: ['javaScript'],
				mode: ['runOnceForEachItem'],
			},
		},
	},
];

export const javascriptCodeDescription: INodeProperties[] = [
	...v1Properties,
	...v2Properties,
	{
		displayName:
			'Type <code>$</code> for a list of <a target="_blank" href="https://docs.n8n.io/code-examples/methods-variables-reference/">special vars/methods</a>. Debug by using <code>console.log()</code> statements and viewing their output in the browser console.',
		name: 'notice',
		type: 'notice',
		displayOptions: {
			show: {
				language: ['javaScript'],
			},
		},
		default: '',
	},
];
