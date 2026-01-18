"""
MIGRATION-META:
  source_path: packages/cli/src/services/role-cache.service.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/services 的服务。导入/依赖:外部:无；内部:@n8n/backend-common、@n8n/constants、@n8n/db、@n8n/di、@n8n/permissions；本地:./cache/cache.service。导出:RoleCacheService。关键函数/方法:buildRoleScopeMap、getRolesWithAllScopes、invalidateCache、refreshCache。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/services/role-cache.service.ts -> services/n8n/application/cli/services/role_cache_service.py

import { Logger } from '@n8n/backend-common';
import { Time } from '@n8n/constants';
import { RoleRepository } from '@n8n/db';
import type { EntityManager } from '@n8n/db';
import { Container, Service } from '@n8n/di';
import { staticRolesWithScope, type Scope } from '@n8n/permissions';

import { CacheService } from './cache/cache.service';

type RoleInfo = {
	scopes: string[]; // array of scope slugs
};

interface RoleScopeMap {
	global?: {
		[roleSlug: string]: RoleInfo;
	};
	project?: {
		[roleSlug: string]: RoleInfo;
	};
	credential?: {
		[roleSlug: string]: RoleInfo;
	};
	workflow?: {
		[roleSlug: string]: RoleInfo;
	};
}

@Service()
export class RoleCacheService {
	private static readonly CACHE_KEY = 'roles:scope-map';
	private static readonly CACHE_TTL = 5 * Time.minutes.toMilliseconds; // 5 minutes TTL

	constructor(
		private readonly cacheService: CacheService,
		private readonly logger: Logger,
	) {}

	/**
	 * Get all roles from database and build scope map
	 */
	private async buildRoleScopeMap(trx?: EntityManager): Promise<RoleScopeMap> {
		try {
			const roleRepository = Container.get(RoleRepository);
			const roles = await roleRepository.findAll(trx);

			const roleScopeMap: RoleScopeMap = {};
			for (const role of roles) {
				roleScopeMap[role.roleType] ??= {};
				roleScopeMap[role.roleType]![role.slug] = {
					scopes: role.scopes.map((s) => s.slug),
				};
			}

			return roleScopeMap;
		} catch (error) {
			this.logger.error('Failed to build role scope from database', { error });
			throw error;
		}
	}

	/**
	 * Get roles with all specified scopes (with caching)
	 */
	async getRolesWithAllScopes(
		namespace: 'global' | 'project' | 'credential' | 'workflow',
		requiredScopes: Scope[],
		em?: EntityManager,
	): Promise<string[]> {
		if (requiredScopes.length === 0) return [];

		// Get cached role map with refresh function
		const roleScopeMap = await this.cacheService.get<RoleScopeMap>(RoleCacheService.CACHE_KEY, {
			refreshFn: async () => await this.buildRoleScopeMap(em),
			fallbackValue: undefined,
		});

		if (roleScopeMap === undefined) {
			// TODO: actively report this case to sentry or similar system
			this.logger.error('Role scope map is undefined, falling back to static roles');
			// Fallback to static roles if dynamic data is not available
			return staticRolesWithScope(namespace, requiredScopes);
		}

		// Filter roles by namespace and scopes
		const matchingRoles: string[] = [];

		for (const [roleSlug, roleInfo] of Object.entries(roleScopeMap[namespace] ?? {})) {
			// Check if role has ALL required scopes
			const hasAllScopes = requiredScopes.every((scope) => roleInfo.scopes.includes(scope));
			if (hasAllScopes) {
				matchingRoles.push(roleSlug);
			}
		}

		return matchingRoles;
	}

	/**
	 * Invalidate the role cache (call after role changes)
	 */
	async invalidateCache(): Promise<void> {
		await this.cacheService.delete(RoleCacheService.CACHE_KEY);
	}

	/**
	 * Force refresh the cache
	 */
	async refreshCache(): Promise<void> {
		const roleScopeMap = await this.buildRoleScopeMap();
		await this.cacheService.set(
			RoleCacheService.CACHE_KEY,
			roleScopeMap,
			RoleCacheService.CACHE_TTL,
		);
	}
}
