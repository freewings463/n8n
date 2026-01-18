"""
MIGRATION-META:
  source_path: packages/cli/src/public-api/v1/handlers/projects/projects.handler.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/public-api/v1/handlers 的模块。导入/依赖:外部:express；内部:@n8n/db、@n8n/di、@/controllers/project.controller、@/errors/…/response.error、@/public-api/types、@/services/project.service.ee；本地:../services/pagination.service。导出:无。关键函数/方法:isLicensed、apiKeyHasScopeWithGlobalScopeFallback、async。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/public-api/v1/handlers/projects/projects.handler.ts -> services/n8n/presentation/cli/api/public-api/v1/handlers/projects/projects_handler.py

import {
	AddUsersToProjectDto,
	ChangeUserRoleInProject,
	CreateProjectDto,
	DeleteProjectDto,
	UpdateProjectWithRelationsDto,
} from '@n8n/api-types';
import type { AuthenticatedRequest } from '@n8n/db';
import { ProjectRepository } from '@n8n/db';
import { Container } from '@n8n/di';
import type { Response } from 'express';

import { ProjectController } from '@/controllers/project.controller';
import { ResponseError } from '@/errors/response-errors/abstract/response.error';
import type { PaginatedRequest } from '@/public-api/types';
import { ProjectService } from '@/services/project.service.ee';

import {
	apiKeyHasScopeWithGlobalScopeFallback,
	isLicensed,
	validCursor,
} from '../../shared/middlewares/global.middleware';
import { encodeNextCursor } from '../../shared/services/pagination.service';

type GetAll = PaginatedRequest;
export = {
	createProject: [
		isLicensed('feat:projectRole:admin'),
		apiKeyHasScopeWithGlobalScopeFallback({ scope: 'project:create' }),
		async (req: AuthenticatedRequest, res: Response) => {
			const payload = CreateProjectDto.safeParse(req.body);
			if (payload.error) {
				return res.status(400).json(payload.error.errors[0]);
			}

			const project = await Container.get(ProjectController).createProject(req, res, payload.data);

			return res.status(201).json(project);
		},
	],
	updateProject: [
		isLicensed('feat:projectRole:admin'),
		apiKeyHasScopeWithGlobalScopeFallback({ scope: 'project:update' }),
		async (req: AuthenticatedRequest<{ projectId: string }>, res: Response) => {
			const payload = UpdateProjectWithRelationsDto.safeParse(req.body);
			if (payload.error) {
				return res.status(400).json(payload.error.errors[0]);
			}

			await Container.get(ProjectController).updateProject(
				req,
				res,
				payload.data,
				req.params.projectId,
			);

			return res.status(204).send();
		},
	],
	deleteProject: [
		isLicensed('feat:projectRole:admin'),
		apiKeyHasScopeWithGlobalScopeFallback({ scope: 'project:delete' }),
		async (req: AuthenticatedRequest<{ projectId: string }>, res: Response) => {
			const query = DeleteProjectDto.safeParse(req.query);
			if (query.error) {
				return res.status(400).json(query.error.errors[0]);
			}

			await Container.get(ProjectController).deleteProject(
				req,
				res,
				query.data,
				req.params.projectId,
			);

			return res.status(204).send();
		},
	],
	getProjects: [
		isLicensed('feat:projectRole:admin'),
		apiKeyHasScopeWithGlobalScopeFallback({ scope: 'project:list' }),
		validCursor,
		async (req: GetAll, res: Response) => {
			const { offset = 0, limit = 100 } = req.query;

			const [projects, count] = await Container.get(ProjectRepository).findAndCount({
				skip: offset,
				take: limit,
			});

			return res.json({
				data: projects,
				nextCursor: encodeNextCursor({
					offset,
					limit,
					numberOfTotalRecords: count,
				}),
			});
		},
	],
	addUsersToProject: [
		isLicensed('feat:projectRole:admin'),
		apiKeyHasScopeWithGlobalScopeFallback({ scope: 'project:update' }),
		async (req: AuthenticatedRequest<{ projectId: string }>, res: Response) => {
			const payload = AddUsersToProjectDto.safeParse(req.body);
			if (payload.error) {
				return res.status(400).json(payload.error.errors[0]);
			}

			try {
				await Container.get(ProjectService).addUsersToProject(
					req.params.projectId,
					payload.data.relations,
				);
			} catch (error) {
				if (error instanceof ResponseError) {
					return res.status(error.httpStatusCode).send({ message: error.message });
				}
				throw error;
			}

			return res.status(201).send();
		},
	],
	changeUserRoleInProject: [
		isLicensed('feat:projectRole:admin'),
		apiKeyHasScopeWithGlobalScopeFallback({ scope: 'project:update' }),
		async (req: AuthenticatedRequest<{ projectId: string; userId: string }>, res: Response) => {
			const payload = ChangeUserRoleInProject.safeParse(req.body);
			if (payload.error) {
				return res.status(400).json(payload.error.errors[0]);
			}

			const { projectId, userId } = req.params;
			const { role } = payload.data;
			try {
				await Container.get(ProjectService).changeUserRoleInProject(projectId, userId, role);
			} catch (error) {
				if (error instanceof ResponseError) {
					return res.status(error.httpStatusCode).send({ message: error.message });
				}
				throw error;
			}

			return res.status(204).send();
		},
	],
	deleteUserFromProject: [
		isLicensed('feat:projectRole:admin'),
		apiKeyHasScopeWithGlobalScopeFallback({ scope: 'project:update' }),
		async (req: AuthenticatedRequest<{ projectId: string; userId: string }>, res: Response) => {
			const { projectId, userId } = req.params;
			try {
				await Container.get(ProjectService).deleteUserFromProject(projectId, userId);
			} catch (error) {
				if (error instanceof ResponseError) {
					return res.status(error.httpStatusCode).send({ message: error.message });
				}
				throw error;
			}
			return res.status(204).send();
		},
	],
};
