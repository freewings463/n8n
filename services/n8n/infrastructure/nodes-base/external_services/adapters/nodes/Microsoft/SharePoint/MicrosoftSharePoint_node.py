"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/SharePoint/MicrosoftSharePoint.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/SharePoint 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./descriptions、./methods。导出:MicrosoftSharePoint。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/SharePoint/MicrosoftSharePoint.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/SharePoint/MicrosoftSharePoint_node.py

import type { INodeType, INodeTypeDescription } from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import { file, item, list } from './descriptions';
import { listSearch, resourceMapping } from './methods';

export class MicrosoftSharePoint implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Microsoft SharePoint',
		name: 'microsoftSharePoint',
		icon: {
			light: 'file:microsoftSharePoint.svg',
			dark: 'file:microsoftSharePoint.svg',
		},
		group: ['transform'],
		version: 1,
		subtitle: '={{ $parameter["operation"] + ": " + $parameter["resource"] }}',
		description: 'Interact with Microsoft SharePoint API',
		defaults: {
			name: 'Microsoft SharePoint',
		},
		usableAsTool: true,
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'microsoftSharePointOAuth2Api',
				required: true,
			},
		],
		requestDefaults: {
			baseURL: '=https://{{ $credentials.subdomain }}.sharepoint.com/_api/v2.0/',
		},
		properties: [
			{
				displayName: 'Resource',
				name: 'resource',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'File',
						value: 'file',
					},
					{
						name: 'Item',
						value: 'item',
					},
					{
						name: 'List',
						value: 'list',
					},
				],
				default: 'file',
			},

			...file.description,
			...item.description,
			...list.description,
		],
	};

	methods = {
		listSearch,
		resourceMapping,
	};
}
