"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/TheHiveProject/actions/page/search.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/TheHiveProject/actions 的节点。导入/依赖:外部:@utils/utilities；内部:无；本地:../helpers/interfaces、../../transport。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/TheHiveProject/actions/page/search.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/TheHiveProject/actions/page/search_operation.py

import type {
	IDataObject,
	IExecuteFunctions,
	INodeExecutionData,
	INodeProperties,
} from 'n8n-workflow';

import { updateDisplayOptions, wrapData } from '@utils/utilities';

import {
	caseRLC,
	genericFiltersCollection,
	returnAllAndLimit,
	sortCollection,
	searchOptions,
} from '../../descriptions';
import type { QueryScope } from '../../helpers/interfaces';
import { theHiveApiQuery } from '../../transport';

const properties: INodeProperties[] = [
	{
		displayName: 'Search in Knowledge Base',
		name: 'searchInKnowledgeBase',
		type: 'boolean',
		default: true,
		description: 'Whether to search in knowledge base or only in the selected case',
	},
	{
		...caseRLC,
		displayOptions: {
			show: {
				searchInKnowledgeBase: [false],
			},
		},
	},
	...returnAllAndLimit,
	genericFiltersCollection,
	sortCollection,
	{
		...searchOptions,
		displayOptions: {
			show: {
				returnAll: [true],
			},
		},
	},
];

const displayOptions = {
	show: {
		resource: ['page'],
		operation: ['search'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, i: number): Promise<INodeExecutionData[]> {
	let responseData: IDataObject | IDataObject[] = [];

	const searchInKnowledgeBase = this.getNodeParameter('searchInKnowledgeBase', i) as boolean;
	const filtersValues = this.getNodeParameter('filters.values', i, []) as IDataObject[];
	const sortFields = this.getNodeParameter('sort.fields', i, []) as IDataObject[];
	const returnAll = this.getNodeParameter('returnAll', i);
	let returnCount = false;
	if (!returnAll) {
		returnCount = this.getNodeParameter('options.returnCount', i, false) as boolean;
	}

	let limit;
	let scope: QueryScope;

	if (searchInKnowledgeBase) {
		scope = { query: 'listOrganisationPage' };
	} else {
		const caseId = this.getNodeParameter('caseId', i, '', { extractValue: true }) as string;
		scope = { query: 'getCase', id: caseId, restrictTo: 'pages' };
	}

	if (!returnAll) {
		limit = this.getNodeParameter('limit', i);
	}

	responseData = await theHiveApiQuery.call(
		this,
		scope,
		filtersValues,
		sortFields,
		limit,
		returnCount,
	);

	const executionData = this.helpers.constructExecutionMetaData(wrapData(responseData), {
		itemData: { item: i },
	});

	return executionData;
}
