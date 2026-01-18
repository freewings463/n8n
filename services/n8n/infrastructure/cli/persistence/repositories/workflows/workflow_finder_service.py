"""
MIGRATION-META:
  source_path: packages/cli/src/workflows/workflow-finder.service.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/workflows 的工作流服务。导入/依赖:外部:无；内部:@n8n/db、@n8n/di、@n8n/permissions、@n8n/typeorm、@/services/role.service；本地:无。导出:WorkflowFinderService。关键函数/方法:findWorkflowForUser、findAllWorkflowsForUser。用于封装工作流业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected TypeORM Repository/EntityManager usage
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/workflows/workflow-finder.service.ts -> services/n8n/infrastructure/cli/persistence/repositories/workflows/workflow_finder_service.py

import type { SharedWorkflow, User } from '@n8n/db';
import { SharedWorkflowRepository, FolderRepository } from '@n8n/db';
import { Service } from '@n8n/di';
import { hasGlobalScope, type Scope } from '@n8n/permissions';
// eslint-disable-next-line n8n-local-rules/misplaced-n8n-typeorm-import
import type { EntityManager, FindOptionsWhere } from '@n8n/typeorm';
// eslint-disable-next-line n8n-local-rules/misplaced-n8n-typeorm-import
import { In } from '@n8n/typeorm';

import { RoleService } from '@/services/role.service';

@Service()
export class WorkflowFinderService {
	constructor(
		private readonly sharedWorkflowRepository: SharedWorkflowRepository,
		private readonly folderRepository: FolderRepository,
		private readonly roleService: RoleService,
	) {}

	async findWorkflowForUser(
		workflowId: string,
		user: User,
		scopes: Scope[],
		options: {
			includeTags?: boolean;
			includeParentFolder?: boolean;
			includeActiveVersion?: boolean;
			em?: EntityManager;
		} = {},
	) {
		let where: FindOptionsWhere<SharedWorkflow> = {};

		if (!hasGlobalScope(user, scopes, { mode: 'allOf' })) {
			const [projectRoles, workflowRoles] = await Promise.all([
				this.roleService.rolesWithScope('project', scopes, options.em),
				this.roleService.rolesWithScope('workflow', scopes, options.em),
			]);

			where = {
				role: In(workflowRoles),
				project: {
					projectRelations: {
						role: In(projectRoles),
						userId: user.id,
					},
				},
			};
		}

		const sharedWorkflow = await this.sharedWorkflowRepository.findWorkflowWithOptions(workflowId, {
			where,
			includeTags: options.includeTags,
			includeParentFolder: options.includeParentFolder,
			includeActiveVersion: options.includeActiveVersion,
			em: options.em,
		});

		if (!sharedWorkflow) {
			return null;
		}

		return sharedWorkflow.workflow;
	}

	async findAllWorkflowsForUser(
		user: User,
		scopes: Scope[],
		folderId?: string,
		projectId?: string,
	) {
		let where: FindOptionsWhere<SharedWorkflow> = {};

		if (folderId) {
			const subFolderIds = await this.folderRepository.getAllFolderIdsInHierarchy(
				folderId,
				projectId,
			);

			where = {
				...where,
				workflow: {
					parentFolder: In([folderId, ...subFolderIds]),
				},
			};
		}

		if (!hasGlobalScope(user, scopes, { mode: 'allOf' })) {
			const [projectRoles, workflowRoles] = await Promise.all([
				this.roleService.rolesWithScope('project', scopes),
				this.roleService.rolesWithScope('workflow', scopes),
			]);

			where = {
				...where,
				role: In(workflowRoles),
				project: {
					...(projectId && { id: projectId }),
					projectRelations: {
						role: In(projectRoles),
						userId: user.id,
					},
				},
			};
		}

		const sharedWorkflows = await this.sharedWorkflowRepository.find({
			where,
			relations: {
				workflow: {
					shared: { project: { projectRelations: { user: true } } },
				},
			},
		});

		return sharedWorkflows.map((sw) => ({ ...sw.workflow, projectId: sw.projectId }));
	}
}
