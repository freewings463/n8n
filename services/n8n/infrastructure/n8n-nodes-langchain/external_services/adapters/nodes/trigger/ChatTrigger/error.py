"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/trigger/ChatTrigger/error.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/trigger/ChatTrigger 的节点。导入/依赖:外部:无；内部:@n8n/errors；本地:无。导出:ChatTriggerAuthorizationError。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/trigger/ChatTrigger/error.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/trigger/ChatTrigger/error.py

import { ApplicationError } from '@n8n/errors';

export class ChatTriggerAuthorizationError extends ApplicationError {
	constructor(
		readonly responseCode: number,
		message?: string,
	) {
		if (message === undefined) {
			message = 'Authorization problem!';
			if (responseCode === 401) {
				message = 'Authorization is required!';
			} else if (responseCode === 403) {
				message = 'Authorization data is wrong!';
			}
		}
		super(message);
	}
}
