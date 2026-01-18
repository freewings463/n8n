"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/repositories/shared-credentials.repository.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/repositories 的仓储。导入/依赖:外部:无；内部:@n8n/di、@n8n/permissions、@n8n/typeorm；本地:../entities。导出:SharedCredentialsRepository。关键函数/方法:findByCredentialIds、makeOwnerOfAllCredentials、makeOwner、deleteByIds、getFilteredAccessibleCredentials、findCredentialOwningProject、getAllRelationsForCredentials、findCredentialsWithOptions、findCredentialsByRoles。用于封装该模块数据读写与查询细节，隔离持久层。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected TypeORM Repository/EntityManager usage
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/repositories/shared-credentials.repository.ts -> services/n8n/infrastructure/n8n-db/persistence/repositories/shared_credentials_repository.py

import { Service } from '@n8n/di';
import type { CredentialSharingRole } from '@n8n/permissions';
import type { EntityManager, FindOptionsWhere } from '@n8n/typeorm';
import { DataSource, In, Not, Repository } from '@n8n/typeorm';

import type { Project } from '../entities';
import { SharedCredentials } from '../entities';

@Service()
export class SharedCredentialsRepository extends Repository<SharedCredentials> {
	constructor(dataSource: DataSource) {
		super(SharedCredentials, dataSource.manager);
	}

	async findByCredentialIds(credentialIds: string[], role: CredentialSharingRole) {
		return await this.find({
			relations: { credentials: true, project: { projectRelations: { user: true, role: true } } },
			where: {
				credentialsId: In(credentialIds),
				role,
			},
		});
	}

	async makeOwnerOfAllCredentials(project: Project) {
		return await this.update(
			{
				projectId: Not(project.id),
				role: 'credential:owner',
			},
			{ project },
		);
	}

	async makeOwner(credentialIds: string[], projectId: string, trx?: EntityManager) {
		trx = trx ?? this.manager;
		return await trx.upsert(
			SharedCredentials,
			credentialIds.map(
				(credentialsId) =>
					({
						projectId,
						credentialsId,
						role: 'credential:owner',
					}) as const,
			),
			['projectId', 'credentialsId'],
		);
	}

	async deleteByIds(sharedCredentialsIds: string[], projectId: string, trx?: EntityManager) {
		trx = trx ?? this.manager;

		return await trx.delete(SharedCredentials, {
			projectId,
			credentialsId: In(sharedCredentialsIds),
		});
	}

	async getFilteredAccessibleCredentials(
		projectIds: string[],
		credentialsIds: string[],
	): Promise<string[]> {
		return (
			await this.find({
				where: {
					projectId: In(projectIds),
					credentialsId: In(credentialsIds),
				},
				select: ['credentialsId'],
			})
		).map((s) => s.credentialsId);
	}

	async findCredentialOwningProject(credentialsId: string) {
		return (
			await this.findOne({
				where: { credentialsId, role: 'credential:owner' },
				relations: { project: true },
			})
		)?.project;
	}

	async getAllRelationsForCredentials(credentialIds: string[]) {
		return await this.find({
			where: {
				credentialsId: In(credentialIds),
			},
			relations: ['project'],
		});
	}

	async findCredentialsWithOptions(
		where: FindOptionsWhere<SharedCredentials> = {},
		trx?: EntityManager,
	) {
		trx = trx ?? this.manager;

		return await trx.find(SharedCredentials, {
			where,
			relations: {
				credentials: {
					shared: { project: { projectRelations: { user: true } } },
				},
			},
		});
	}

	async findCredentialsByRoles(
		userIds: string[],
		projectRoles: string[],
		credentialRoles: string[],
		trx?: EntityManager,
	) {
		trx = trx ?? this.manager;

		return await trx.find(SharedCredentials, {
			where: {
				role: In(credentialRoles),
				project: {
					projectRelations: {
						userId: In(userIds),
						role: { slug: In(projectRoles) },
					},
				},
			},
		});
	}
}
