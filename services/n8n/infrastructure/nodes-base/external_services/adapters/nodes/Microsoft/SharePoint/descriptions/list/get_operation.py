"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/SharePoint/descriptions/list/get.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/SharePoint 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../common.descriptions。导出:description。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/SharePoint/descriptions/list/get.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/SharePoint/descriptions/list/get_operation.py

import { updateDisplayOptions, type INodeProperties } from 'n8n-workflow';

import { listRLC, siteRLC, untilSiteSelected } from '../common.descriptions';

const properties: INodeProperties[] = [
	{
		...siteRLC,
		description: 'Select the site to retrieve lists from',
	},
	{
		...listRLC,
		description: 'Select the list you want to retrieve',
		displayOptions: {
			hide: {
				...untilSiteSelected,
			},
		},
	},
	{
		displayName: 'Simplify',
		name: 'simplify',
		default: true,
		routing: {
			send: {
				property: '$select',
				type: 'query',
				value:
					'={{ $value ? "id,name,displayName,description,createdDateTime,lastModifiedDateTime,webUrl" : undefined }}',
			},
		},
		type: 'boolean',
	},
];

const displayOptions = {
	show: {
		resource: ['list'],
		operation: ['get'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);
