"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/N8n/WorkflowLocator.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/N8n 的工作流节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./GenericFunctions。导出:workflowIdLocator。关键函数/方法:searchWorkflows、searchResults、workflows。用于实现 n8n 工作流节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/N8n/WorkflowLocator.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/N8n/WorkflowLocator.py

import type { ILoadOptionsFunctions, INodeListSearchResult, INodeProperties } from 'n8n-workflow';

import { apiRequestAllItems } from './GenericFunctions';

type DataItemsResponse<T> = {
	data: T[];
};

interface PartialWorkflow {
	id: number;
	name: string;
}

/**
 * A helper to populate workflow lists. It does a pseudo-search by
 * listing available workflows and matching with the specified query.
 */
export async function searchWorkflows(
	this: ILoadOptionsFunctions,
	query?: string,
): Promise<INodeListSearchResult> {
	const searchResults = (await apiRequestAllItems.call(
		this,
		'GET',
		'workflows',
		{},
	)) as DataItemsResponse<PartialWorkflow>;

	// Map the workflows list against a simple name/id filter, and sort
	// with the latest on top.
	const workflows = (searchResults as unknown as PartialWorkflow[])
		.map((w: PartialWorkflow) => ({
			name: `${w.name} (#${w.id})`,
			value: w.id,
		}))
		.filter(
			(w) =>
				!query ||
				w.name.toLowerCase().includes(query.toLowerCase()) ||
				w.value?.toString() === query,
		)
		.sort((a, b) => b.value - a.value);

	return {
		results: workflows,
	};
}

/**
 * A resourceLocator to enable looking up workflows by their ID.
 * This object can be used as a base and then extended as needed.
 */
export const workflowIdLocator: INodeProperties = {
	displayName: 'Workflow',
	name: 'workflowId',
	type: 'resourceLocator',
	default: { mode: 'list', value: '' },
	description: 'Workflow to filter the executions by',
	modes: [
		{
			displayName: 'From List',
			name: 'list',
			type: 'list',
			placeholder: 'Select a Workflow...',
			initType: 'workflow',
			typeOptions: {
				searchListMethod: 'searchWorkflows',
				searchFilterRequired: false,
				searchable: true,
			},
		},
		{
			displayName: 'By URL',
			name: 'url',
			type: 'string',
			placeholder: 'https://myinstance.app.n8n.cloud/workflow/1',
			validation: [
				{
					type: 'regex',
					properties: {
						regex: '.*/workflow/([0-9a-zA-Z]{1,})',
						errorMessage: 'Not a valid Workflow URL',
					},
				},
			],
			extractValue: {
				type: 'regex',
				regex: '.*/workflow/([0-9a-zA-Z]{1,})',
			},
		},
		{
			displayName: 'ID',
			name: 'id',
			type: 'string',
			validation: [
				{
					type: 'regex',
					properties: {
						regex: '[0-9a-zA-Z]{1,}',
						errorMessage: 'Not a valid Workflow ID',
					},
				},
			],
			placeholder: '1',
		},
	],
};
