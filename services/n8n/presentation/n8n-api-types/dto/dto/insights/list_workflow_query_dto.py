"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/dto/insights/list-workflow-query.dto.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/dto/insights 的工作流模块。导入/依赖:外部:zod、zod-class；内部:无；本地:../pagination/pagination.dto。导出:MAX_ITEMS_PER_PAGE、ListInsightsWorkflowQueryDto。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/dto/insights/list-workflow-query.dto.ts -> services/n8n/presentation/n8n-api-types/dto/dto/insights/list_workflow_query_dto.py

import { z } from 'zod';
import { Z } from 'zod-class';

import { createTakeValidator, paginationSchema } from '../pagination/pagination.dto';

export const MAX_ITEMS_PER_PAGE = 100;

const VALID_SORT_OPTIONS = [
	'total:asc',
	'total:desc',
	'succeeded:asc',
	'succeeded:desc',
	'failed:asc',
	'failed:desc',
	'failureRate:asc',
	'failureRate:desc',
	'timeSaved:asc',
	'timeSaved:desc',
	'runTime:asc',
	'runTime:desc',
	'averageRunTime:asc',
	'averageRunTime:desc',
	'workflowName:asc',
	'workflowName:desc',
] as const;

// ---------------------
// Parameter Validators
// ---------------------

const sortByValidator = z
	.enum(VALID_SORT_OPTIONS, { message: `sortBy must be one of: ${VALID_SORT_OPTIONS.join(', ')}` })
	.optional();

export class ListInsightsWorkflowQueryDto extends Z.class({
	...paginationSchema,
	take: createTakeValidator(MAX_ITEMS_PER_PAGE),
	startDate: z.coerce.date().optional(),
	endDate: z.coerce.date().optional(),
	sortBy: sortByValidator,
	projectId: z.string().optional(),
}) {}
