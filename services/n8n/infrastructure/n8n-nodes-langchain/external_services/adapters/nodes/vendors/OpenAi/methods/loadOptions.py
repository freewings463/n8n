"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/methods/loadOptions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/OpenAi 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../transport。导出:无。关键函数/方法:getFiles。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/methods/loadOptions.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/OpenAi/methods/loadOptions.py

import type { ILoadOptionsFunctions, INodePropertyOptions } from 'n8n-workflow';

import { apiRequest } from '../transport';

export async function getFiles(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
	const { data } = await apiRequest.call(this, 'GET', '/files', { qs: { purpose: 'assistants' } });

	const returnData: INodePropertyOptions[] = [];

	for (const file of data || []) {
		returnData.push({
			name: file.filename as string,
			value: file.id as string,
		});
	}

	return returnData;
}
