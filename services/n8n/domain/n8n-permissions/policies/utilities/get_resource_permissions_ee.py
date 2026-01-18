"""
MIGRATION-META:
  source_path: packages/@n8n/permissions/src/utilities/get-resource-permissions.ee.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/@n8n/permissions/src/utilities 的模块。导入/依赖:外部:无；内部:无；本地:../constants.ee、../types.ee。导出:PermissionsRecord、getResourcePermissions。关键函数/方法:getResourcePermissions。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/permissions treated as domain authorization policies
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/permissions/src/utilities/get-resource-permissions.ee.ts -> services/n8n/domain/n8n-permissions/policies/utilities/get_resource_permissions_ee.py

import { RESOURCES } from '../constants.ee';
import type { Scope } from '../types.ee';

type ExtractScopePrefixSuffix<T> = T extends `${infer Prefix}:${infer Suffix}`
	? [Prefix, Suffix]
	: never;
type ActionBooleans<T extends readonly string[]> = {
	[K in T[number]]?: boolean;
};
export type PermissionsRecord = {
	[K in keyof typeof RESOURCES]: ActionBooleans<(typeof RESOURCES)[K]>;
};

export const getResourcePermissions = (resourceScopes: Scope[] = []): PermissionsRecord =>
	Object.keys(RESOURCES).reduce(
		(permissions, key) => ({
			...permissions,
			[key]: resourceScopes.reduce((resourcePermissions, scope) => {
				const [prefix, suffix] = scope.split(':') as ExtractScopePrefixSuffix<Scope>;

				if (prefix === key) {
					return {
						...resourcePermissions,
						[suffix]: true,
					};
				}

				return resourcePermissions;
			}, {}),
		}),
		{} as PermissionsRecord,
	);
