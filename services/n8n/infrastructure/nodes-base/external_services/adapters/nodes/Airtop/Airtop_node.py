"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtop/Airtop.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtop 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../agent/Agent.resource、../extraction/Extraction.resource、../file/File.resource、../interaction/Interaction.resource 等3项。导出:Airtop。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtop/Airtop.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtop/Airtop_node.py

import { NodeConnectionTypes } from 'n8n-workflow';
import type { IExecuteFunctions, INodeType, INodeTypeDescription } from 'n8n-workflow';

import * as agent from './actions/agent/Agent.resource';
import * as extraction from './actions/extraction/Extraction.resource';
import * as file from './actions/file/File.resource';
import * as interaction from './actions/interaction/Interaction.resource';
import { router } from './actions/router';
import * as session from './actions/session/Session.resource';
import * as window from './actions/window/Window.resource';

export class Airtop implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Airtop',
		name: 'airtop',
		icon: 'file:airtop.svg',
		group: ['transform'],
		defaultVersion: 1,
		version: [1, 1.1],
		subtitle: '={{ $parameter["operation"] + ": " + $parameter["resource"] }}',
		description: 'Scrape and control any site with Airtop',
		usableAsTool: true,
		defaults: {
			name: 'Airtop',
		},
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'airtopApi',
				required: true,
			},
		],
		properties: [
			{
				displayName: 'Resource',
				name: 'resource',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Agent',
						value: 'agent',
					},
					{
						name: 'Extraction',
						value: 'extraction',
					},
					{
						name: 'File',
						value: 'file',
					},
					{
						name: 'Interaction',
						value: 'interaction',
					},
					{
						name: 'Session',
						value: 'session',
					},
					{
						name: 'Window',
						value: 'window',
					},
				],
				default: 'session',
			},
			...agent.description,
			...session.description,
			...window.description,
			...file.description,
			...extraction.description,
			...interaction.description,
		],
	};

	async execute(this: IExecuteFunctions) {
		return await router.call(this);
	}
}
