"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtop/actions/extraction/scrape.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtop/actions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../common/session.utils。导出:无。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtop/actions/extraction/scrape.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtop/actions/extraction/scrape_operation.py

import type { IExecuteFunctions, INodeExecutionData } from 'n8n-workflow';

import { executeRequestWithSessionManagement } from '../common/session.utils';

export async function execute(
	this: IExecuteFunctions,
	index: number,
): Promise<INodeExecutionData[]> {
	const result = await executeRequestWithSessionManagement.call(this, index, {
		method: 'POST',
		path: '/sessions/{sessionId}/windows/{windowId}/scrape-content',
		body: {},
	});

	return this.helpers.returnJsonArray({ ...result });
}
