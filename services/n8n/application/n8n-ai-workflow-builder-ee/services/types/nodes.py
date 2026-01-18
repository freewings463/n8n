"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/types/nodes.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/types 的工作流类型。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:NodeDetails、NodeSearchResult、AddedNode。关键函数/方法:无。用于定义工作流相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/types/nodes.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/types/nodes.py

import type { INodeParameters, INodeProperties, INodeTypeDescription } from 'n8n-workflow';

/**
 * Detailed information about a node type
 */
export interface NodeDetails {
	name: string;
	displayName: string;
	description: string;
	properties: INodeProperties[];
	subtitle?: string;
	inputs: INodeTypeDescription['inputs'];
	outputs: INodeTypeDescription['outputs'];
}

/**
 * Node search result with scoring
 */
export interface NodeSearchResult {
	name: string;
	displayName: string;
	description: string;
	version: number;
	score: number;
	inputs: INodeTypeDescription['inputs'];
	outputs: INodeTypeDescription['outputs'];
}

/**
 * Information about a node that was added to the workflow
 */
export interface AddedNode {
	id: string;
	name: string;
	type: string;
	displayName?: string;
	parameters?: INodeParameters;
	position: [number, number];
}
