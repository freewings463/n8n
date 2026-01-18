"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/repositories/role.repository.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/repositories 的仓储。导入/依赖:外部:无；内部:@n8n/config、@n8n/di、@n8n/typeorm、n8n-workflow；本地:../entities。导出:RoleRepository。关键函数/方法:findAll、countUsersWithRole、findAllRoleCounts、findBySlug、findBySlugs、removeBySlug、updateEntityWithManager、updateRole。用于封装该模块数据读写与查询细节，隔离持久层。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected TypeORM Repository/EntityManager usage
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/repositories/role.repository.ts -> services/n8n/infrastructure/n8n-db/persistence/repositories/role_repository.py

import { DatabaseConfig } from '@n8n/config';
import { Service } from '@n8n/di';
import { DataSource, EntityManager, In, Repository } from '@n8n/typeorm';
import { UserError } from 'n8n-workflow';

import { ProjectRelation, Role, User } from '../entities';

@Service()
export class RoleRepository extends Repository<Role> {
	constructor(
		dataSource: DataSource,
		private readonly databaseConfig: DatabaseConfig,
	) {
		super(Role, dataSource.manager);
	}

	async findAll(trx?: EntityManager) {
		const em = trx ?? this.manager;
		return await em.find(Role, { relations: ['scopes'] });
	}

	async countUsersWithRole(role: Role): Promise<number> {
		if (role.roleType === 'global') {
			return await this.manager.getRepository(User).count({
				where: {
					role: {
						slug: role.slug,
					},
				},
			});
		} else if (role.roleType === 'project') {
			return await this.manager.getRepository(ProjectRelation).count({
				where: { role: { slug: role.slug } },
			});
		}

		return 0;
	}

	async findAllRoleCounts() {
		const userCount = await this.manager
			.createQueryBuilder(User, 'user')
			.select('user.roleSlug', 'roleSlug')
			.addSelect('COUNT(user.id)', 'count')
			.groupBy('user.roleSlug')
			.getRawMany<{ roleSlug: string; count: string }>();

		const projectCount = await this.manager
			.createQueryBuilder(ProjectRelation, 'projectRelation')
			.select('projectRelation.role', 'roleSlug')
			.addSelect('COUNT(projectRelation.user)', 'count')
			.groupBy('projectRelation.role')
			.getRawMany<{ roleSlug: string; count: string }>();

		return userCount.concat(projectCount).reduce(
			(acc, { roleSlug, count }) => {
				if (!acc[roleSlug]) {
					acc[roleSlug] = 0;
				}
				acc[roleSlug] += parseInt(count, 10);
				return acc;
			},
			{} as Record<string, number>,
		);
	}

	async findBySlug(slug: string) {
		return await this.findOne({
			where: { slug },
			relations: ['scopes'],
		});
	}

	async findBySlugs(slugs: string[], roleType: 'global' | 'project' | 'workflow' | 'credential') {
		return await this.find({
			where: { slug: In(slugs), roleType },
			relations: ['scopes'],
		});
	}

	async removeBySlug(slug: string) {
		const result = await this.delete({ slug });
		if (result.affected !== 1) {
			throw new Error(`Failed to delete role "${slug}"`);
		}
	}

	private async updateEntityWithManager(
		entityManager: EntityManager,
		slug: string,
		newData: Partial<Pick<Role, 'description' | 'scopes' | 'displayName'>>,
	) {
		const role = await entityManager.findOne(Role, {
			where: { slug },
			relations: ['scopes'],
		});
		if (!role) {
			throw new UserError('Role not found');
		}
		if (role.systemRole) {
			throw new UserError('Cannot update system roles');
		}

		// Only update fields that are explicitly provided (not undefined)
		// This preserves existing scopes when scopes is undefined
		if (newData.displayName !== undefined) {
			role.displayName = newData.displayName;
		}

		if (newData.description !== undefined) {
			role.description = newData.description;
		}

		if (newData.scopes !== undefined) {
			role.scopes = newData.scopes;
		}

		return await entityManager.save<Role>(role);
	}

	async updateRole(
		slug: string,
		newData: Partial<Pick<Role, 'description' | 'scopes' | 'displayName'>>,
	) {
		// Do not use transactions for sqlite legacy
		if (this.databaseConfig.isLegacySqlite) {
			return await this.updateEntityWithManager(this.manager, slug, newData);
		}
		return await this.manager.transaction(async (transactionManager) => {
			return await this.updateEntityWithManager(transactionManager, slug, newData);
		});
	}
}
