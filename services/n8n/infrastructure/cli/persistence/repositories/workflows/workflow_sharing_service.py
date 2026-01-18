"""
MIGRATION-META:
  source_path: packages/cli/src/workflows/workflow-sharing.service.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/workflows 的工作流服务。导入/依赖:外部:无；内部:@n8n/db、@n8n/di、@n8n/typeorm、@/services/role.service；本地:无。导出:ShareWorkflowOptions、WorkflowSharingService。关键函数/方法:getSharedWorkflowIds、getSharedWithMeIds、getSharedWorkflowScopes、getOwnedWorkflowsInPersonalProject。用于封装工作流业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected TypeORM Repository/EntityManager usage
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/workflows/workflow-sharing.service.ts -> services/n8n/infrastructure/cli/persistence/repositories/workflows/workflow_sharing_service.py

import type { User } from '@n8n/db';
import { ProjectRelationRepository, SharedWorkflowRepository } from '@n8n/db';
import { Service } from '@n8n/di';
import {
	hasGlobalScope,
	type ProjectRole,
	type WorkflowSharingRole,
	type Scope,
	PROJECT_OWNER_ROLE_SLUG,
} from '@n8n/permissions';
// eslint-disable-next-line n8n-local-rules/misplaced-n8n-typeorm-import
import { In } from '@n8n/typeorm';

import { RoleService } from '@/services/role.service';

export type ShareWorkflowOptions =
	| { scopes: Scope[]; projectId?: string }
	| { projectRoles: ProjectRole[]; workflowRoles: WorkflowSharingRole[]; projectId?: string };

@Service()
export class WorkflowSharingService {
	constructor(
		private readonly sharedWorkflowRepository: SharedWorkflowRepository,
		private readonly roleService: RoleService,
		private readonly projectRelationRepository: ProjectRelationRepository,
	) {}

	/**
	 * Get the IDs of the workflows that have been shared with the user based on
	 * scope or roles.
	 * If `scopes` is passed the roles are inferred. Alternatively `projectRoles`
	 * and `workflowRoles` can be passed specifically.
	 *
	 * Returns all IDs if user has the 'workflow:read' global scope.
	 */

	async getSharedWorkflowIds(user: User, options: ShareWorkflowOptions): Promise<string[]> {
		const { projectId } = options;

		if (hasGlobalScope(user, 'workflow:read')) {
			const sharedWorkflows = await this.sharedWorkflowRepository.find({
				select: ['workflowId'],
				...(projectId && { where: { projectId } }),
			});
			return sharedWorkflows.map(({ workflowId }) => workflowId);
		}

		const projectRoles =
			'scopes' in options
				? await this.roleService.rolesWithScope('project', options.scopes)
				: options.projectRoles;
		const workflowRoles =
			'scopes' in options
				? await this.roleService.rolesWithScope('workflow', options.scopes)
				: options.workflowRoles;

		const sharedWorkflows = await this.sharedWorkflowRepository.find({
			where: {
				role: In(workflowRoles),
				project: {
					projectRelations: {
						userId: user.id,
						role: In(projectRoles),
					},
				},
			},
			select: ['workflowId'],
		});

		return sharedWorkflows.map(({ workflowId }) => workflowId);
	}

	async getSharedWithMeIds(user: User) {
		const sharedWithMeWorkflows = await this.sharedWorkflowRepository.find({
			select: ['workflowId'],
			where: {
				role: 'workflow:editor',
				project: {
					projectRelations: {
						userId: user.id,
						role: { slug: PROJECT_OWNER_ROLE_SLUG },
					},
				},
			},
		});

		return sharedWithMeWorkflows.map(({ workflowId }) => workflowId);
	}

	async getSharedWorkflowScopes(
		workflowIds: string[],
		user: User,
	): Promise<Array<[string, Scope[]]>> {
		const projectRelations = await this.projectRelationRepository.findAllByUser(user.id);
		const sharedWorkflows =
			await this.sharedWorkflowRepository.getRelationsByWorkflowIdsAndProjectIds(
				workflowIds,
				projectRelations.map((p) => p.projectId),
			);

		return workflowIds.map((workflowId) => {
			return [
				workflowId,
				this.roleService.combineResourceScopes(
					'workflow',
					user,
					sharedWorkflows.filter((s) => s.workflowId === workflowId),
					projectRelations,
				),
			];
		});
	}

	async getOwnedWorkflowsInPersonalProject(user: User): Promise<string[]> {
		const sharedWorkflows = await this.sharedWorkflowRepository.find({
			select: ['workflowId'],
			where: {
				role: 'workflow:owner',
				project: {
					projectRelations: {
						userId: user.id,
						role: { slug: PROJECT_OWNER_ROLE_SLUG },
					},
				},
			},
		});
		return sharedWorkflows.map(({ workflowId }) => workflowId);
	}
}
