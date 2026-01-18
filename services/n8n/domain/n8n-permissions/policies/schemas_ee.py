"""
MIGRATION-META:
  source_path: packages/@n8n/permissions/src/schemas.ee.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/@n8n/permissions/src 的模块。导入/依赖:外部:zod；内部:无；本地:./scope-information。导出:roleNamespaceSchema、globalRoleSchema、assignableGlobalRoleSchema、personalRoleSchema、teamRoleSchema、customProjectRoleSchema、systemProjectRoleSchema、assignableProjectRoleSchema 等6项。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/permissions treated as domain authorization policies
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/permissions/src/schemas.ee.ts -> services/n8n/domain/n8n-permissions/policies/schemas_ee.py

import { z } from 'zod';

import { ALL_SCOPES } from './scope-information';

export const roleNamespaceSchema = z.enum(['global', 'project', 'credential', 'workflow']);

export const globalRoleSchema = z.enum([
	'global:owner',
	'global:admin',
	'global:member',
	'global:chatUser',
]);

const customGlobalRoleSchema = z
	.string()
	.nonempty()
	.refine((val) => !globalRoleSchema.safeParse(val).success, {
		message: 'This global role value is not assignable',
	});

export const assignableGlobalRoleSchema = z.union([
	globalRoleSchema.exclude([
		'global:owner', // Owner cannot be changed
	]),
	customGlobalRoleSchema,
]);

export const personalRoleSchema = z.enum([
	'project:personalOwner', // personalOwner is only used for personal projects
]);

// Those are the system roles for projects assignable to a user
export const teamRoleSchema = z.enum([
	'project:admin',
	'project:editor',
	'project:viewer',
	'project:chatUser',
]);

// Custom project role can be anything but the system roles
export const customProjectRoleSchema = z
	.string()
	.nonempty()
	.refine((val) => !systemProjectRoleSchema.safeParse(val).success, {
		message: 'This global role value is not assignable',
	});

// Those are all the system roles for projects
export const systemProjectRoleSchema = z.union([personalRoleSchema, teamRoleSchema]);

// Those are the roles that can be assigned to a user for a project (all roles except personalOwner)
export const assignableProjectRoleSchema = z.union([teamRoleSchema, customProjectRoleSchema]);

export const projectRoleSchema = z.union([systemProjectRoleSchema, customProjectRoleSchema]);

export const credentialSharingRoleSchema = z.enum(['credential:owner', 'credential:user']);

export const workflowSharingRoleSchema = z.enum(['workflow:owner', 'workflow:editor']);

const ALL_SCOPES_LOOKUP_SET = new Set(ALL_SCOPES as string[]);

export const scopeSchema = z.string().refine((val) => ALL_SCOPES_LOOKUP_SET.has(val), {
	message: 'Invalid scope',
});

export const roleSchema = z.object({
	slug: z.string().min(1),
	displayName: z.string().min(1),
	description: z.string().nullable(),
	systemRole: z.boolean(),
	roleType: roleNamespaceSchema,
	licensed: z.boolean(),
	scopes: z.array(scopeSchema),
	createdAt: z.date().optional(),
	updatedAt: z.date().optional(),
	usedByUsers: z.number().optional(),
});

export type Role = z.infer<typeof roleSchema>;
