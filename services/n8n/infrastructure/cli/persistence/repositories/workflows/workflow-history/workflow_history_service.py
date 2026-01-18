"""
MIGRATION-META:
  source_path: packages/cli/src/workflows/workflow-history/workflow-history.service.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/workflows/workflow-history 的工作流服务。导入/依赖:外部:无；内部:@n8n/backend-common、@n8n/db、@n8n/di、@n8n/typeorm、n8n-workflow、@/errors/shared-workflow-not-found.error 等1项；本地:../workflow-finder.service。导出:WorkflowHistoryService。关键函数/方法:getList、getVersion、findVersion、saveVersion、updateVersion、getVersionsByIds。用于封装工作流业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected TypeORM Repository/EntityManager usage
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/workflows/workflow-history/workflow-history.service.ts -> services/n8n/infrastructure/cli/persistence/repositories/workflows/workflow-history/workflow_history_service.py

import { Logger } from '@n8n/backend-common';
import type { User, WorkflowHistoryUpdate } from '@n8n/db';
import { WorkflowHistory, WorkflowHistoryRepository } from '@n8n/db';
import { Service } from '@n8n/di';
// eslint-disable-next-line n8n-local-rules/misplaced-n8n-typeorm-import
import type { EntityManager } from '@n8n/typeorm';
// eslint-disable-next-line n8n-local-rules/misplaced-n8n-typeorm-import
import { In } from '@n8n/typeorm';
import type { IWorkflowBase } from 'n8n-workflow';
import { ensureError, UnexpectedError } from 'n8n-workflow';

import { WorkflowFinderService } from '../workflow-finder.service';

import { SharedWorkflowNotFoundError } from '@/errors/shared-workflow-not-found.error';
import { WorkflowHistoryVersionNotFoundError } from '@/errors/workflow-history-version-not-found.error';

@Service()
export class WorkflowHistoryService {
	constructor(
		private readonly logger: Logger,
		private readonly workflowHistoryRepository: WorkflowHistoryRepository,
		private readonly workflowFinderService: WorkflowFinderService,
	) {}

	async getList(
		user: User,
		workflowId: string,
		take: number,
		skip: number,
	): Promise<Array<Omit<WorkflowHistory, 'nodes' | 'connections'>>> {
		const workflow = await this.workflowFinderService.findWorkflowForUser(workflowId, user, [
			'workflow:read',
		]);

		if (!workflow) {
			throw new SharedWorkflowNotFoundError('');
		}

		return await this.workflowHistoryRepository.find({
			where: {
				workflowId: workflow.id,
			},
			take,
			skip,
			select: [
				'workflowId',
				'versionId',
				'authors',
				'createdAt',
				'updatedAt',
				'name',
				'description',
			],
			relations: ['workflowPublishHistory'],
			order: { createdAt: 'DESC' },
		});
	}

	async getVersion(
		user: User,
		workflowId: string,
		versionId: string,
		settings?: { includePublishHistory?: boolean },
	): Promise<WorkflowHistory> {
		const workflow = await this.workflowFinderService.findWorkflowForUser(workflowId, user, [
			'workflow:read',
		]);

		if (!workflow) {
			throw new SharedWorkflowNotFoundError('');
		}

		const includePublishHistory = settings?.includePublishHistory ?? true;
		const relations = includePublishHistory ? ['workflowPublishHistory'] : [];

		const hist = await this.workflowHistoryRepository.findOne({
			where: {
				workflowId: workflow.id,
				versionId,
			},
			relations,
		});
		if (!hist) {
			throw new WorkflowHistoryVersionNotFoundError('');
		}
		return hist;
	}

	/**
	 * Find a workflow history version without permission checks.
	 */
	async findVersion(workflowId: string, versionId: string): Promise<WorkflowHistory | null> {
		return await this.workflowHistoryRepository.findOne({
			where: {
				workflowId,
				versionId,
			},
		});
	}

	async saveVersion(
		user: User | string,
		workflow: IWorkflowBase,
		workflowId: string,
		autosaved = false,
		transactionManager?: EntityManager,
	) {
		if (!workflow.nodes || !workflow.connections) {
			throw new UnexpectedError(
				`Cannot save workflow history: nodes and connections are required for workflow ${workflowId}`,
			);
		}

		const authors = typeof user === 'string' ? user : `${user.firstName} ${user.lastName}`;

		const repository = transactionManager
			? transactionManager.getRepository(WorkflowHistory)
			: this.workflowHistoryRepository;

		try {
			await repository.insert({
				authors,
				connections: workflow.connections,
				nodes: workflow.nodes,
				versionId: workflow.versionId,
				workflowId,
				autosaved,
			});
		} catch (e) {
			const error = ensureError(e);
			this.logger.error(`Failed to save workflow history version for workflow ${workflowId}`, {
				error,
			});
		}
	}

	async updateVersion(versionId: string, workflowId: string, updateData: WorkflowHistoryUpdate) {
		await this.workflowHistoryRepository.update({ versionId, workflowId }, { ...updateData });
	}

	/**
	 * Get multiple versions by their IDs
	 * Returns only versions that exist, skipping non-existent ones
	 */
	async getVersionsByIds(
		user: User,
		workflowId: string,
		versionIds: string[],
	): Promise<Array<{ versionId: string; createdAt: Date }>> {
		if (versionIds.length === 0) {
			return [];
		}

		const workflow = await this.workflowFinderService.findWorkflowForUser(workflowId, user, [
			'workflow:read',
		]);

		if (!workflow) {
			throw new SharedWorkflowNotFoundError('');
		}

		const versions = await this.workflowHistoryRepository.find({
			where: {
				workflowId: workflow.id,
				versionId: In(versionIds),
			},
			select: ['versionId', 'createdAt'],
		});

		return versions.map((v) => ({ versionId: v.versionId, createdAt: v.createdAt }));
	}
}
