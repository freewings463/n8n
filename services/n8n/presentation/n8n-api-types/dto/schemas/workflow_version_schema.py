"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/schemas/workflow-version.schema.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/schemas 的工作流模块。导入/依赖:外部:zod；内部:无；本地:无。导出:WORKFLOW_VERSION_NAME_MAX_LENGTH、WORKFLOW_VERSION_DESCRIPTION_MAX_LENGTH、workflowVersionNameSchema、workflowVersionDescriptionSchema。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/schemas/workflow-version.schema.ts -> services/n8n/presentation/n8n-api-types/dto/schemas/workflow_version_schema.py

import { z } from 'zod';

export const WORKFLOW_VERSION_NAME_MAX_LENGTH = 128;
export const WORKFLOW_VERSION_DESCRIPTION_MAX_LENGTH = 2048;

export const workflowVersionNameSchema = z
	.string()
	.max(WORKFLOW_VERSION_NAME_MAX_LENGTH, {
		message: `Version name cannot be longer than ${WORKFLOW_VERSION_NAME_MAX_LENGTH} characters`,
	})
	.optional();

export const workflowVersionDescriptionSchema = z
	.string()
	.max(WORKFLOW_VERSION_DESCRIPTION_MAX_LENGTH, {
		message: `Version description cannot be longer than ${WORKFLOW_VERSION_DESCRIPTION_MAX_LENGTH} characters`,
	})
	.optional();
