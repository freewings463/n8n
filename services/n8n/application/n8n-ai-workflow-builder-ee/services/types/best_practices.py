"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/types/best-practices.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/types 的工作流类型。导入/依赖:外部:无；内部:无；本地:./categorization。导出:BestPracticesDocument。关键函数/方法:getDocumentation。用于定义工作流相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/types/best-practices.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/types/best_practices.py

import type { WorkflowTechniqueType } from './categorization';

/**
 * Interface for best practices documentation for a specific workflow technique
 */
export interface BestPracticesDocument {
	/** The workflow technique this documentation covers */
	readonly technique: WorkflowTechniqueType;

	/** Version of the documentation */
	readonly version: string;

	/**
	 * Returns the full documentation as a markdown-formatted string
	 */
	getDocumentation(): string;
}
