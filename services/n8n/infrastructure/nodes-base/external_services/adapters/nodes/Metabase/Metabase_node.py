"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Metabase/Metabase.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Metabase 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./AlertsDescription、./DatabasesDescription、./MetricsDescription、./QuestionsDescription。导出:Metabase。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Metabase/Metabase.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Metabase/Metabase_node.py

import type { INodeType, INodeTypeDescription } from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import { alertsFields, alertsOperations } from './AlertsDescription';
import { databasesFields, databasesOperations } from './DatabasesDescription';
import { metricsFields, metricsOperations } from './MetricsDescription';
import { questionsFields, questionsOperations } from './QuestionsDescription';

export class Metabase implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Metabase',
		name: 'metabase',
		icon: 'file:metabase.svg',
		group: ['transform'],
		version: 1,
		subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
		description: 'Use the Metabase API',
		defaults: {
			name: 'Metabase',
		},
		usableAsTool: true,
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'metabaseApi',
				required: true,
			},
		],
		requestDefaults: {
			returnFullResponse: true,
			baseURL: '={{$credentials.url.replace(new RegExp("/$"), "")}}',
			headers: {},
		},
		properties: [
			{
				displayName: 'Resource',
				name: 'resource',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Alert',
						value: 'alerts',
					},
					{
						name: 'Database',
						value: 'databases',
					},
					{
						name: 'Metric',
						value: 'metrics',
					},
					{
						name: 'Question',
						value: 'questions',
					},
				],
				default: 'questions',
			},
			...questionsOperations,
			...questionsFields,
			...metricsOperations,
			...metricsFields,
			...databasesOperations,
			...databasesFields,
			...alertsOperations,
			...alertsFields,
		],
	};
}
