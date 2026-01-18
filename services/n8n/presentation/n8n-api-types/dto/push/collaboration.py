"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/push/collaboration.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/push 的模块。导入/依赖:外部:无；内部:无；本地:../datetime、../user。导出:Collaborator、CollaboratorsChanged、WriteAccessAcquired、WriteAccessReleased、CollaborationPushMessage。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/push/collaboration.ts -> services/n8n/presentation/n8n-api-types/dto/push/collaboration.py

import type { Iso8601DateTimeString } from '../datetime';
import type { MinimalUser } from '../user';

export type Collaborator = {
	user: MinimalUser;
	lastSeen: Iso8601DateTimeString;
};

export type CollaboratorsChanged = {
	type: 'collaboratorsChanged';
	data: {
		workflowId: string;
		collaborators: Collaborator[];
	};
};

export type WriteAccessAcquired = {
	type: 'writeAccessAcquired';
	data: {
		workflowId: string;
		userId: string;
	};
};

export type WriteAccessReleased = {
	type: 'writeAccessReleased';
	data: {
		workflowId: string;
	};
};

export type CollaborationPushMessage =
	| CollaboratorsChanged
	| WriteAccessAcquired
	| WriteAccessReleased;
