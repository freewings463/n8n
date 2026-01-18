"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/schemas/banner-name.schema.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/schemas 的模块。导入/依赖:外部:zod；内部:无；本地:无。导出:staticBannerNameSchema、dynamicBannerNameSchema、bannerNameSchema、BannerName。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/schemas/banner-name.schema.ts -> services/n8n/presentation/n8n-api-types/dto/schemas/banner_name_schema.py

import { z } from 'zod';

export const staticBannerNameSchema = z.enum([
	'V1',
	'TRIAL_OVER',
	'TRIAL',
	'NON_PRODUCTION_LICENSE',
	'EMAIL_CONFIRMATION',
	'DATA_TABLE_STORAGE_LIMIT_WARNING',
	'DATA_TABLE_STORAGE_LIMIT_ERROR',
	'WORKFLOW_AUTO_DEACTIVATED',
]);
export const dynamicBannerNameSchema = z.string().regex(/^dynamic-banner-\d+$/);
export const bannerNameSchema = z.union([staticBannerNameSchema, dynamicBannerNameSchema]);

export type BannerName = z.infer<typeof bannerNameSchema>;
