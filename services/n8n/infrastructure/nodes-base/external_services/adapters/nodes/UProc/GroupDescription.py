"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/UProc/GroupDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/UProc 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./Json/Groups。导出:groupOptions。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/UProc/GroupDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/UProc/GroupDescription.py

import type { IDataObject, INodeProperties } from 'n8n-workflow';

import { groups } from './Json/Groups';

const finalGroups = {
	displayName: 'Resource',
	name: 'group',
	type: 'options',
	default: 'communication',
	options: [],
};

const options = [];

for (const group of (groups as IDataObject).groups as IDataObject[]) {
	const item = {
		name: group.translated,
		value: group.name,
		description:
			'The ' +
			(group.translated as string) +
			' Resource allows you to get tools from this resource',
	};
	options.push(item);
}

//@ts-ignore
finalGroups.options = options;
const mappedGroups = [finalGroups];

export const groupOptions = mappedGroups as INodeProperties[];
