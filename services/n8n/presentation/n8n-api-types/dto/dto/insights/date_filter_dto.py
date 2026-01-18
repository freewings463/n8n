"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/dto/insights/date-filter.dto.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/dto/insights 的Insights模块。导入/依赖:外部:zod、zod-class；内部:无；本地:无。导出:InsightsDateFilterDto。关键函数/方法:无。用于承载Insights实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/dto/insights/date-filter.dto.ts -> services/n8n/presentation/n8n-api-types/dto/dto/insights/date_filter_dto.py

import { z } from 'zod';
import { Z } from 'zod-class';

export class InsightsDateFilterDto extends Z.class({
	startDate: z.coerce.date().optional(),
	endDate: z.coerce.date().optional(),
	projectId: z.string().optional(),
}) {}
