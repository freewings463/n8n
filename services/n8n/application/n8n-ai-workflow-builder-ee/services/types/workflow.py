"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/types/workflow.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/types 的工作流类型。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:SimpleWorkflow、WorkflowOperation。关键函数/方法:无。用于定义工作流相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/types/workflow.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/types/workflow.py

import type { IWorkflowBase, INode, IConnections } from 'n8n-workflow';

/**
 * Simplified workflow representation containing only nodes and connections
 */
export type SimpleWorkflow = Pick<IWorkflowBase, 'name' | 'nodes' | 'connections'>;

/**
 * Workflow operation types that can be applied to the workflow state
 */
export type WorkflowOperation =
	| { type: 'clear' }
	| { type: 'removeNode'; nodeIds: string[] }
	| { type: 'addNodes'; nodes: INode[] }
	| { type: 'updateNode'; nodeId: string; updates: Partial<INode> }
	| { type: 'setConnections'; connections: IConnections }
	| { type: 'mergeConnections'; connections: IConnections }
	| {
			type: 'removeConnection';
			sourceNode: string;
			targetNode: string;
			connectionType: string;
			sourceOutputIndex: number;
			targetInputIndex: number;
	  }
	| { type: 'setName'; name: string };
