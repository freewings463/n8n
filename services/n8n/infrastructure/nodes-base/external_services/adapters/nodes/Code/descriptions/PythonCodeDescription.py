"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Code/descriptions/PythonCodeDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Code/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:pythonCodeDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Code/descriptions/PythonCodeDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Code/descriptions/PythonCodeDescription.py

import type { INodeProperties } from 'n8n-workflow';

const commonDescription: INodeProperties = {
	displayName: 'Python',
	name: 'pythonCode',
	type: 'string',
	typeOptions: {
		editor: 'codeNodeEditor',
		editorLanguage: 'python',
	},
	default: '',
	description:
		'Python code to execute.<br><br>Tip: You can use built-in methods and variables like <code>_today</code> for dates and <code>_jmespath</code> for querying JSON structures. <a href="https://docs.n8n.io/code/builtin/">Learn more</a>.',
	noDataExpression: true,
};

const PRINT_INSTRUCTION =
	'Debug by using <code>print()</code> statements and viewing their output in the browser console.';

export const pythonCodeDescription: INodeProperties[] = [
	{
		...commonDescription,
		displayOptions: {
			show: {
				language: ['pythonNative'],
				mode: ['runOnceForAllItems'],
			},
		},
	},
	{
		...commonDescription,
		displayOptions: {
			show: {
				language: ['pythonNative'],
				mode: ['runOnceForEachItem'],
			},
		},
	},
	{
		displayName: `${PRINT_INSTRUCTION}<br><br>The Python option does not support <code>_</code> syntax and helpers, except for <code>_items</code> in all-items mode and <code>_item</code> in per-item mode.`,
		name: 'notice',
		type: 'notice',
		displayOptions: {
			show: {
				language: ['pythonNative'],
			},
		},
		default: '',
	},
];
