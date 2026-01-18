"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Evaluation/methods/listSearch.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Evaluation/methods 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../common/methods。再导出:../methods/listSearch。导出:无。关键函数/方法:dataTableSearch。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Evaluation/methods/listSearch.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Evaluation/methods/listSearch.py

import type { ILoadOptionsFunctions, INodeListSearchResult } from 'n8n-workflow';

import { tableSearch } from '../../DataTable/common/methods';

export * from './../../Google/Sheet/v2/methods/listSearch';

export async function dataTableSearch(
	this: ILoadOptionsFunctions,
	filterString?: string,
	prevPaginationToken?: string,
): Promise<INodeListSearchResult> {
	return await tableSearch.call(this, filterString, prevPaginationToken);
}
