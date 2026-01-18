"""
MIGRATION-META:
  source_path: packages/cli/src/public-api/v1/handlers/users/users.handler.ee.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/public-api/v1/handlers 的模块。导入/依赖:外部:express；内部:@n8n/api-types、@n8n/db、@n8n/di、@/controllers/invitation.controller、@/controllers/users.controller、@/events/event.service 等1项；本地:./users.service.ee、../services/pagination.service。导出:无。关键函数/方法:apiKeyHasScopeWithGlobalScopeFallback、async、isLicensed。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/public-api/v1/handlers/users/users.handler.ee.ts -> services/n8n/presentation/cli/api/public-api/v1/handlers/users/users_handler_ee.py

import { InviteUsersRequestDto, RoleChangeRequestDto } from '@n8n/api-types';
import type { AuthenticatedRequest } from '@n8n/db';
import { ProjectRelationRepository } from '@n8n/db';
import { Container } from '@n8n/di';
import type express from 'express';
import type { Response } from 'express';

import { InvitationController } from '@/controllers/invitation.controller';
import { UsersController } from '@/controllers/users.controller';
import { EventService } from '@/events/event.service';
import type { UserRequest } from '@/requests';

import { clean, getAllUsersAndCount, getUser } from './users.service.ee';
import {
	apiKeyHasScopeWithGlobalScopeFallback,
	isLicensed,
	validCursor,
	validLicenseWithUserQuota,
} from '../../shared/middlewares/global.middleware';
import { encodeNextCursor } from '../../shared/services/pagination.service';

type Create = AuthenticatedRequest<{}, {}, InviteUsersRequestDto>;
type Delete = UserRequest.Delete;
type ChangeRole = AuthenticatedRequest<{ id: string }, {}, RoleChangeRequestDto, {}>;

export = {
	getUser: [
		validLicenseWithUserQuota,
		apiKeyHasScopeWithGlobalScopeFallback({ scope: 'user:read' }),
		async (req: UserRequest.Get, res: express.Response) => {
			const { includeRole = false } = req.query;
			const { id } = req.params;

			const user = await getUser({ withIdentifier: id, includeRole });

			if (!user) {
				return res.status(404).json({
					message: `Could not find user with id: ${id}`,
				});
			}

			Container.get(EventService).emit('user-retrieved-user', {
				userId: req.user.id,
				publicApi: true,
			});

			return res.json(clean(user, { includeRole }));
		},
	],
	getUsers: [
		apiKeyHasScopeWithGlobalScopeFallback({ scope: 'user:list' }),
		validLicenseWithUserQuota,
		validCursor,
		async (req: UserRequest.Get, res: express.Response) => {
			const { offset = 0, limit = 100, includeRole = false, projectId } = req.query;

			const _in = projectId
				? await Container.get(ProjectRelationRepository).findUserIdsByProjectId(projectId)
				: undefined;

			const [users, count] = await getAllUsersAndCount({
				includeRole,
				limit,
				offset,
				in: _in,
			});

			Container.get(EventService).emit('user-retrieved-all-users', {
				userId: req.user.id,
				publicApi: true,
			});

			return res.json({
				data: clean(users, { includeRole }),
				nextCursor: encodeNextCursor({
					offset,
					limit,
					numberOfTotalRecords: count,
				}),
			});
		},
	],
	createUser: [
		apiKeyHasScopeWithGlobalScopeFallback({ scope: 'user:create' }),
		async (req: Create, res: Response) => {
			const { data, error } = InviteUsersRequestDto.safeParse(req.body);
			if (error) {
				return res.status(400).json(error.errors[0]);
			}

			const usersInvited = await Container.get(InvitationController).inviteUser(
				req,
				res,
				data as InviteUsersRequestDto,
			);
			return res.status(201).json(usersInvited);
		},
	],
	deleteUser: [
		apiKeyHasScopeWithGlobalScopeFallback({ scope: 'user:delete' }),
		async (req: Delete, res: Response) => {
			await Container.get(UsersController).deleteUser(req);

			return res.status(204).send();
		},
	],
	changeRole: [
		isLicensed('feat:advancedPermissions'),
		apiKeyHasScopeWithGlobalScopeFallback({ scope: 'user:changeRole' }),
		async (req: ChangeRole, res: Response) => {
			const validation = RoleChangeRequestDto.safeParse(req.body);
			if (validation.error) {
				return res.status(400).json({
					message: validation.error.errors[0],
				});
			}

			await Container.get(UsersController).changeGlobalRole(
				req,
				res,
				validation.data,
				req.params.id,
			);

			return res.status(204).send();
		},
	],
};
