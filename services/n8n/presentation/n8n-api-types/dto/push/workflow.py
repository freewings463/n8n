"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/push/workflow.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/push 的工作流模块。导入/依赖:外部:无；内部:无；本地:无。导出:WorkflowActivated、WorkflowFailedToActivate、WorkflowDeactivated、WorkflowAutoDeactivated、WorkflowUpdated、WorkflowPushMessage。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/push/workflow.ts -> services/n8n/presentation/n8n-api-types/dto/push/workflow.py

export type WorkflowActivated = {
	type: 'workflowActivated';
	data: {
		workflowId: string;
		activeVersionId: string;
	};
};

export type WorkflowFailedToActivate = {
	type: 'workflowFailedToActivate';
	data: {
		workflowId: string;
		errorMessage: string;
	};
};

export type WorkflowDeactivated = {
	type: 'workflowDeactivated';
	data: {
		workflowId: string;
	};
};

export type WorkflowAutoDeactivated = {
	type: 'workflowAutoDeactivated';
	data: {
		workflowId: string;
	};
};

export type WorkflowUpdated = {
	type: 'workflowUpdated';
	data: {
		workflowId: string;
		userId: string;
	};
};

export type WorkflowPushMessage =
	| WorkflowActivated
	| WorkflowFailedToActivate
	| WorkflowDeactivated
	| WorkflowAutoDeactivated
	| WorkflowUpdated;
