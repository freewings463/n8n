"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/E2eTest/mock.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/E2eTest 的节点。导入/依赖:外部:minifaker、minifaker/…/en；内部:无；本地:无。导出:returnData、remoteOptions、resourceMapperFields、searchOptions。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/E2eTest/mock.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/E2eTest/mock.py

import { array, name, uuid } from 'minifaker';
import 'minifaker/locales/en';
import type {
	INodeExecutionData,
	INodeListSearchResult,
	INodePropertyOptions,
	ResourceMapperFields,
} from 'n8n-workflow';

export const returnData: INodeExecutionData[] = [
	{
		json: {
			id: '23423532',
			name: 'Hello World',
		},
	},
];

export const remoteOptions: INodePropertyOptions[] = [
	{
		name: 'Resource 1',
		value: 'resource1',
	},
	{
		name: 'Resource 2',
		value: 'resource2',
	},
	{
		name: 'Resource 3',
		value: 'resource3',
	},
];

export const resourceMapperFields: ResourceMapperFields = {
	fields: [
		{
			id: 'id',
			displayName: 'ID',
			defaultMatch: true,
			canBeUsedToMatch: true,
			required: true,
			display: true,
			type: 'string',
		},
		{
			id: 'name',
			displayName: 'Name',
			defaultMatch: false,
			canBeUsedToMatch: false,
			required: false,
			display: true,
			type: 'string',
		},
		{
			id: 'age',
			displayName: 'Age',
			defaultMatch: false,
			canBeUsedToMatch: false,
			required: false,
			display: true,
			type: 'number',
		},
	],
};

export const searchOptions: INodeListSearchResult['results'] = array(100, () => {
	const value = uuid.v4();
	return {
		name: name(),
		value,
		url: 'https://example.com/user/' + value,
	};
});
