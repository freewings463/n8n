"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/schemas/user-settings.schema.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/schemas 的模块。导入/依赖:外部:zod；内部:无；本地:无。导出:npsSurveyRespondedSchema、npsSurveyWaitingSchema、npsSurveySchema、userSettingsSchema、UserSettings。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/schemas/user-settings.schema.ts -> services/n8n/presentation/n8n-api-types/dto/schemas/user_settings_schema.py

import { z } from 'zod';

export const npsSurveyRespondedSchema = z.object({
	lastShownAt: z.number(),
	responded: z.literal(true),
});

export const npsSurveyWaitingSchema = z.object({
	lastShownAt: z.number(),
	waitingForResponse: z.literal(true),
	ignoredCount: z.number(),
});

export const npsSurveySchema = z.union([npsSurveyRespondedSchema, npsSurveyWaitingSchema]);

export const userSettingsSchema = z.object({
	isOnboarded: z.boolean().optional(),
	firstSuccessfulWorkflowId: z.string().optional(),
	userActivated: z.boolean().optional(),
	userActivatedAt: z.number().optional(),
	allowSSOManualLogin: z.boolean().optional(),
	npsSurvey: npsSurveySchema.optional(),
	easyAIWorkflowOnboarded: z.boolean().optional(),
	userClaimedAiCredits: z.boolean().optional(),
	dismissedCallouts: z.record(z.boolean()).optional(),
});
export type UserSettings = z.infer<typeof userSettingsSchema>;
