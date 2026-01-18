"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ERPNext/utils.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ERPNext 的节点。导入/依赖:外部:lodash/flow、lodash/sortBy、lodash/uniqBy；内部:无；本地:无。导出:DocumentProperties、processNames、toSQL。关键函数/方法:ensureName、sortByName、uniqueByName、toSQL。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ERPNext/utils.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/ERPNext/utils.py

import flow from 'lodash/flow';
import sortBy from 'lodash/sortBy';
import uniqBy from 'lodash/uniqBy';

export type DocumentProperties = {
	customProperty: Array<{ field: string; value: string }>;
};

type DocFields = Array<{ name: string; value: string }>;

const ensureName = (docFields: DocFields) => docFields.filter((o) => o.name);
const sortByName = (docFields: DocFields) => sortBy(docFields, ['name']);
const uniqueByName = (docFields: DocFields) => uniqBy(docFields, (o) => o.name);

export const processNames = flow(ensureName, sortByName, uniqueByName);

export const toSQL = (operator: string) => {
	const operators: { [key: string]: string } = {
		is: '=',
		isNot: '!=',
		greater: '>',
		less: '<',
		equalsGreater: '>=',
		equalsLess: '<=',
	};

	return operators[operator];
};
