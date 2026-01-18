"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Outlook/v2/actions/node.type.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Outlook 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:MicrosoftOutlook。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Outlook/v2/actions/node.type.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Outlook/v2/actions/node_type.py

import type { AllEntities } from 'n8n-workflow';

type NodeMap = {
	calendar: 'create' | 'delete' | 'get' | 'getAll' | 'update';
	contact: 'create' | 'delete' | 'get' | 'getAll' | 'update';
	draft: 'create' | 'delete' | 'get' | 'send' | 'update';
	event: 'create' | 'delete' | 'get' | 'getAll' | 'update';
	folder: 'create' | 'delete' | 'get' | 'getAll' | 'update';
	folderMessage: 'getAll';
	message: 'delete' | 'get' | 'getAll' | 'move' | 'update' | 'send' | 'reply' | 'sendAndWait';
	messageAttachment: 'add' | 'download' | 'getAll' | 'get';
};

export type MicrosoftOutlook = AllEntities<NodeMap>;
