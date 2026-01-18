"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/dto/data-table/update-data-table-row.dto.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/dto/data-table 的模块。导入/依赖:外部:zod、zod-class；内部:无；本地:../schemas/data-table-filter.schema。导出:UpdateDataTableRowDto。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/dto/data-table/update-data-table-row.dto.ts -> services/n8n/presentation/n8n-api-types/dto/dto/data-table/update_data_table_row_dto.py

import { z } from 'zod';
import { Z } from 'zod-class';

import { dataTableFilterSchema } from '../../schemas/data-table-filter.schema';
import {
	dataTableColumnNameSchema,
	dataTableColumnValueSchema,
} from '../../schemas/data-table.schema';

const updateFilterSchema = dataTableFilterSchema.refine((filter) => filter.filters.length > 0, {
	message: 'filter must not be empty',
});

const updateDataTableRowShape = {
	filter: updateFilterSchema,
	data: z
		.record(dataTableColumnNameSchema, dataTableColumnValueSchema)
		.refine((obj) => Object.keys(obj).length > 0, {
			message: 'data must not be empty',
		}),
	returnData: z.boolean().optional().default(false),
	dryRun: z.boolean().optional().default(false),
};

export class UpdateDataTableRowDto extends Z.class(updateDataTableRowShape) {}
