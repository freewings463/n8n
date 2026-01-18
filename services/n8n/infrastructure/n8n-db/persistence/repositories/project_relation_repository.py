"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/repositories/project-relation.repository.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/repositories 的仓储。导入/依赖:外部:无；内部:@n8n/di、@n8n/permissions、@n8n/typeorm；本地:../entities。导出:ProjectRelationRepository。关键函数/方法:getPersonalProjectOwners、getPersonalProjectsForUsers、getAccessibleProjectsByRoles、findProjectRole、countUsersByRole、rows、findUserIdsByProjectId、findAllByUser。用于封装该模块数据读写与查询细节，隔离持久层。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected TypeORM Repository/EntityManager usage
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/repositories/project-relation.repository.ts -> services/n8n/infrastructure/n8n-db/persistence/repositories/project_relation_repository.py

import { Service } from '@n8n/di';
import { PROJECT_OWNER_ROLE_SLUG, type ProjectRole } from '@n8n/permissions';
import { DataSource, In, Repository } from '@n8n/typeorm';

import { ProjectRelation } from '../entities';

@Service()
export class ProjectRelationRepository extends Repository<ProjectRelation> {
	constructor(dataSource: DataSource) {
		super(ProjectRelation, dataSource.manager);
	}

	async getPersonalProjectOwners(projectIds: string[]) {
		return await this.find({
			where: {
				projectId: In(projectIds),
				role: { slug: PROJECT_OWNER_ROLE_SLUG },
			},
			relations: {
				user: {
					role: true,
				},
			},
		});
	}

	async getPersonalProjectsForUsers(userIds: string[]) {
		const projectRelations = await this.find({
			where: {
				userId: In(userIds),
				role: { slug: PROJECT_OWNER_ROLE_SLUG },
			},
		});

		return projectRelations.map((pr) => pr.projectId);
	}

	async getAccessibleProjectsByRoles(userId: string, roles: string[]) {
		const projectRelations = await this.find({
			where: { userId, role: { slug: In(roles) } },
		});

		return projectRelations.map((pr) => pr.projectId);
	}

	/**
	 * Find the role of a user in a project.
	 */
	async findProjectRole({ userId, projectId }: { userId: string; projectId: string }) {
		const relation = await this.findOneBy({ projectId, userId });

		return relation?.role ?? null;
	}

	/** Counts the number of users in each role, e.g. `{ admin: 2, member: 6, owner: 1 }` */
	async countUsersByRole() {
		const rows = (await this.createQueryBuilder()
			.select(['role', 'COUNT(role) as count'])
			.groupBy('role')
			.execute()) as Array<{ role: ProjectRole; count: string }>;
		return rows.reduce(
			(acc, row) => {
				acc[row.role] = parseInt(row.count, 10);
				return acc;
			},
			{} as Record<ProjectRole, number>,
		);
	}

	async findUserIdsByProjectId(projectId: string): Promise<string[]> {
		const rows = await this.find({
			select: ['userId'],
			where: { projectId },
		});

		return [...new Set(rows.map((r) => r.userId))];
	}

	async findAllByUser(userId: string) {
		return await this.find({
			where: {
				userId,
			},
			relations: { role: true },
		});
	}
}
