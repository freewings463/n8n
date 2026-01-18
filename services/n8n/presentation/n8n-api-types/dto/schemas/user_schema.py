"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/schemas/user.schema.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/schemas 的模块。导入/依赖:外部:zod；内部:@n8n/permissions；本地:./user-settings.schema。导出:ROLE、Role、roleSchema、userProjectSchema、userBaseSchema、userDetailSchema、usersListSchema、User 等1项。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/schemas/user.schema.ts -> services/n8n/presentation/n8n-api-types/dto/schemas/user_schema.py

import { projectRoleSchema } from '@n8n/permissions';
import { z } from 'zod';

import { userSettingsSchema } from './user-settings.schema';

export const ROLE = {
	Owner: 'global:owner',
	Member: 'global:member',
	Admin: 'global:admin',
	ChatUser: 'global:chatUser',
	Default: 'default', // default user with no email when setting up instance
} as const;

export type Role = (typeof ROLE)[keyof typeof ROLE];

// Ensuring the array passed to z.enum is correctly typed as non-empty.
const roleValuesForSchema = Object.values(ROLE) as [Role, ...Role[]];
export const roleSchema = z.enum(roleValuesForSchema);

export const userProjectSchema = z.object({
	id: z.string(),
	role: projectRoleSchema,
	name: z.string(),
});

export const userBaseSchema = z.object({
	id: z.string(),
	firstName: z.string().nullable().optional(),
	lastName: z.string().nullable().optional(),
	email: z.string().email().nullable().optional(),
	role: roleSchema.optional(),
});

export const userDetailSchema = userBaseSchema.extend({
	isPending: z.boolean().optional(),
	isOwner: z.boolean().optional(),
	signInType: z.string().optional(),
	settings: userSettingsSchema.nullable().optional(),
	personalizationAnswers: z.object({}).passthrough().nullable().optional(),
	projectRelations: z.array(userProjectSchema).nullable().optional(),
	mfaEnabled: z.boolean().optional(),
	lastActiveAt: z.string().nullable().optional(),
	inviteAcceptUrl: z.string().optional(),
});

export const usersListSchema = z.object({
	count: z.number(),
	items: z.array(userDetailSchema),
});

export type User = z.infer<typeof userDetailSchema>;
export type UsersList = z.infer<typeof usersListSchema>;
