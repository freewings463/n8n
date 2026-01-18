"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtop/actions/extraction/Extraction.resource.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtop/actions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./getPaginated.operation、./query.operation、./scrape.operation、../common/fields。导出:getPaginated、query、scrape、description。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtop/actions/extraction/Extraction.resource.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtop/actions/extraction/Extraction_resource.py

import type { INodeProperties } from 'n8n-workflow';

import * as getPaginated from './getPaginated.operation';
import * as query from './query.operation';
import * as scrape from './scrape.operation';
import { getSessionModeFields } from '../common/fields';

export { getPaginated, query, scrape };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['extraction'],
			},
		},
		options: [
			{
				name: 'Query Page',
				value: 'query',
				description: 'Query a page to extract data or ask a question given the data on the page',
				action: 'Query page',
			},
			{
				name: 'Query Page with Pagination',
				value: 'getPaginated',
				description: 'Extract content from paginated or dynamically loaded pages',
				action: 'Query page with pagination',
			},
			{
				name: 'Smart Scrape',
				value: 'scrape',
				description: 'Scrape a page and return the data as markdown',
				action: 'Smart scrape page',
			},
		],
		default: 'getPaginated',
	},
	...getSessionModeFields('extraction', ['getPaginated', 'query', 'scrape']),
	...getPaginated.description,
	...query.description,
];
