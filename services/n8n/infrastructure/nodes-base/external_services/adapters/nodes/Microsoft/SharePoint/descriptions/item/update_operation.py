"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/SharePoint/descriptions/item/update.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/SharePoint 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../helpers/utils、../common.descriptions。导出:description。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/SharePoint/descriptions/item/update.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/SharePoint/descriptions/item/update_operation.py

import { updateDisplayOptions, type INodeProperties } from 'n8n-workflow';

import { itemColumnsPreSend } from '../../helpers/utils';
import { listRLC, siteRLC, untilListSelected, untilSiteSelected } from '../common.descriptions';

const properties: INodeProperties[] = [
	{
		...siteRLC,
		description: 'Select the site to retrieve lists from',
	},
	{
		...listRLC,
		description: 'Select the list you want to update an item in',
		displayOptions: {
			hide: {
				...untilSiteSelected,
			},
		},
	},
	{
		displayName:
			'Due to API restrictions, the following column types cannot be updated: Hyperlink, Location, Metadata',
		name: 'noticeUnsupportedFields',
		displayOptions: {
			hide: {
				...untilSiteSelected,
				...untilListSelected,
			},
		},
		type: 'notice',
		default: '',
	},
	{
		displayName: 'Columns',
		name: 'columns',
		default: {
			mappingMode: 'defineBelow',
			value: null,
		},
		displayOptions: {
			hide: {
				...untilSiteSelected,
				...untilListSelected,
			},
		},
		noDataExpression: true,
		required: true,
		routing: {
			send: {
				preSend: [itemColumnsPreSend],
			},
		},
		type: 'resourceMapper',
		typeOptions: {
			loadOptionsDependsOn: ['site.value', 'list.value'],
			resourceMapper: {
				resourceMapperMethod: 'getMappingColumns',
				mode: 'update',
				fieldWords: {
					singular: 'column',
					plural: 'columns',
				},
				addAllFields: true,
				multiKeyMatch: false,
			},
		},
	},
];

const displayOptions = {
	show: {
		resource: ['item'],
		operation: ['update'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);
