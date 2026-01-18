"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/SharePoint/descriptions/common.descriptions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/SharePoint 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:untilFolderSelected、untilItemSelected、untilListSelected、untilSiteSelected、fileRLC、folderRLC、itemRLC、listRLC 等1项。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/SharePoint/descriptions/common.descriptions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/SharePoint/descriptions/common_descriptions.py

import type { INodeProperties } from 'n8n-workflow';

export const untilFolderSelected = { folder: [''] };

export const untilItemSelected = { item: [''] };

export const untilListSelected = { list: [''] };

export const untilSiteSelected = { site: [''] };

export const fileRLC: INodeProperties = {
	displayName: 'File',
	name: 'file',
	default: {
		mode: 'list',
		value: '',
	},
	description: 'Select the file to download',
	modes: [
		{
			displayName: 'From List',
			name: 'list',
			type: 'list',
			typeOptions: {
				searchListMethod: 'getFiles',
				searchable: true,
			},
		},
		{
			displayName: 'By ID',
			name: 'id',
			placeholder: 'e.g. mysite',
			type: 'string',
		},
	],
	placeholder: 'eg. my-file.pdf',
	required: true,
	type: 'resourceLocator',
};

export const folderRLC: INodeProperties = {
	displayName: 'Parent Folder',
	name: 'folder',
	default: {
		mode: 'list',
		value: '',
	},
	description: 'Select the folder to update the file in',
	modes: [
		{
			displayName: 'From List',
			name: 'list',
			type: 'list',
			typeOptions: {
				searchListMethod: 'getFolders',
				searchable: true,
			},
		},
		{
			displayName: 'By ID',
			name: 'id',
			placeholder: 'e.g. myfolder',
			type: 'string',
		},
	],
	placeholder: '/ (Library root)',
	required: true,
	type: 'resourceLocator',
};

export const itemRLC: INodeProperties = {
	displayName: 'Item',
	name: 'item',
	default: {
		mode: 'list',
		value: '',
	},
	description: 'Select the item you want to delete',
	modes: [
		{
			displayName: 'From List',
			name: 'list',
			type: 'list',
			typeOptions: {
				searchListMethod: 'getItems',
				searchable: true,
			},
		},
		{
			displayName: 'By ID',
			name: 'id',
			placeholder: 'e.g. 1',
			type: 'string',
		},
	],
	required: true,
	type: 'resourceLocator',
};

export const listRLC: INodeProperties = {
	displayName: 'List',
	name: 'list',
	default: {
		mode: 'list',
		value: '',
	},
	description: 'Select the list you want to retrieve',
	modes: [
		{
			displayName: 'From List',
			name: 'list',
			type: 'list',
			typeOptions: {
				searchListMethod: 'getLists',
				searchable: true,
			},
		},
		{
			displayName: 'By ID',
			name: 'id',
			placeholder: 'e.g. mylist',
			type: 'string',
		},
	],
	required: true,
	type: 'resourceLocator',
};

export const siteRLC: INodeProperties = {
	displayName: 'Site',
	name: 'site',
	default: {
		mode: 'list',
		value: '',
	},
	description: 'Select the site to retrieve folders from',
	modes: [
		{
			displayName: 'From List',
			name: 'list',
			type: 'list',
			typeOptions: {
				searchListMethod: 'getSites',
				searchable: true,
			},
		},
		{
			displayName: 'By ID',
			name: 'id',
			placeholder: 'e.g. mysite',
			type: 'string',
		},
	],
	required: true,
	type: 'resourceLocator',
};
