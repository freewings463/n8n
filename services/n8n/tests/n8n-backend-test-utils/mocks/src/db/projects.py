"""
MIGRATION-META:
  source_path: packages/@n8n/backend-test-utils/src/db/projects.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/backend-test-utils/src/db 的模块。导入/依赖:外部:无；内部:@n8n/db、@n8n/di 等1项；本地:../random。导出:linkUserToProject、createTeamProject、getPersonalProject、findProject、getProjectRelations、getProjectRoleForUser、getAllProjectRelations。关键函数/方法:linkUserToProject、createTeamProject、getProjectByNameOrFail、getPersonalProject、findProject、getProjectRelations、getProjectRoleForUser 等1项。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Test utilities package -> tests/mocks
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/backend-test-utils/src/db/projects.ts -> services/n8n/tests/n8n-backend-test-utils/mocks/src/db/projects.py

import type { Project, User, ProjectRelation } from '@n8n/db';
import { ProjectRelationRepository, ProjectRepository } from '@n8n/db';
import { Container } from '@n8n/di';
import type { AssignableProjectRole } from '@n8n/permissions';
import { PROJECT_OWNER_ROLE_SLUG } from '@n8n/permissions';

import { randomName } from '../random';

export const linkUserToProject = async (
	user: User,
	project: Project,
	role: AssignableProjectRole,
) => {
	const projectRelationRepository = Container.get(ProjectRelationRepository);
	await projectRelationRepository.save(
		projectRelationRepository.create({
			projectId: project.id,
			userId: user.id,
			role: { slug: role },
		}),
	);
};

export const createTeamProject = async (name?: string, adminUser?: User) => {
	const projectRepository = Container.get(ProjectRepository);
	const project = await projectRepository.save(
		projectRepository.create({
			name: name ?? randomName(),
			type: 'team',
			creatorId: adminUser?.id,
		}),
	);

	if (adminUser) {
		await linkUserToProject(adminUser, project, 'project:admin');
	}

	return project;
};

export async function getProjectByNameOrFail(name: string) {
	return await Container.get(ProjectRepository).findOneOrFail({ where: { name } });
}

export const getPersonalProject = async (user: User): Promise<Project> => {
	return await Container.get(ProjectRepository).findOneOrFail({
		where: {
			projectRelations: {
				userId: user.id,
				role: { slug: PROJECT_OWNER_ROLE_SLUG },
			},
			type: 'personal',
		},
	});
};

export const findProject = async (id: string): Promise<Project> => {
	return await Container.get(ProjectRepository).findOneOrFail({
		where: { id },
	});
};

export const getProjectRelations = async ({
	projectId,
	userId,
	role,
}: Partial<ProjectRelation>): Promise<ProjectRelation[]> => {
	return await Container.get(ProjectRelationRepository).find({
		where: { projectId, userId, role },
		relations: { role: true },
	});
};

export const getProjectRoleForUser = async (
	projectId: string,
	userId: string,
): Promise<AssignableProjectRole | undefined> => {
	return (
		await Container.get(ProjectRelationRepository).findOne({
			where: { projectId, userId },
			relations: { role: true },
		})
	)?.role?.slug;
};

export const getAllProjectRelations = async ({
	projectId,
}: Partial<ProjectRelation>): Promise<ProjectRelation[]> => {
	return await Container.get(ProjectRelationRepository).find({
		where: { projectId },
		relations: { role: true },
	});
};
