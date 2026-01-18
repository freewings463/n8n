"""
MIGRATION-META:
  source_path: packages/cli/src/modules/chat-hub/chat-session.repository.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/modules/chat-hub 的仓储。导入/依赖:外部:无；内部:@n8n/di、@n8n/typeorm、@/errors/…/not-found.error；本地:./chat-hub-session.entity。导出:ChatHubSessionRepository。关键函数/方法:createChatSession、updateChatSession、deleteChatHubSession、getManyByUserId、existsById、getOneById、deleteAll。用于封装该模块数据读写与查询细节，隔离持久层。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected TypeORM Repository/EntityManager usage
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/chat-hub/chat-session.repository.ts -> services/n8n/infrastructure/cli/persistence/repositories/modules/chat-hub/chat_session_repository.py

import { Service } from '@n8n/di';
import { DataSource, EntityManager, Repository } from '@n8n/typeorm';

import { ChatHubSession, IChatHubSession } from './chat-hub-session.entity';

import { NotFoundError } from '@/errors/response-errors/not-found.error';

@Service()
export class ChatHubSessionRepository extends Repository<ChatHubSession> {
	constructor(dataSource: DataSource) {
		super(ChatHubSession, dataSource.manager);
	}

	async createChatSession(
		session: Partial<IChatHubSession> & Pick<IChatHubSession, 'id'>,
		trx?: EntityManager,
	) {
		const em = trx ?? this.manager;
		await em.insert(ChatHubSession, session);
		return await em.findOneOrFail(ChatHubSession, {
			where: { id: session.id },
			relations: ['messages'],
		});
	}

	async updateChatSession(id: string, updates: Partial<IChatHubSession>, trx?: EntityManager) {
		const em = trx ?? this.manager;
		await em.update(ChatHubSession, { id }, updates);
	}

	async deleteChatHubSession(id: string, trx?: EntityManager) {
		const em = trx ?? this.manager;
		return await em.delete(ChatHubSession, { id });
	}

	async getManyByUserId(userId: string, limit: number, cursor?: string) {
		const queryBuilder = this.createQueryBuilder('session')
			.leftJoinAndSelect('session.agent', 'agent')
			.leftJoinAndSelect('session.workflow', 'workflow')
			.leftJoinAndSelect('workflow.activeVersion', 'activeVersion')
			.where('session.ownerId = :userId', { userId })
			.orderBy('session.lastMessageAt', 'DESC')
			.addOrderBy('session.id', 'ASC');

		if (cursor) {
			const cursorSession = await this.findOne({
				where: { id: cursor, ownerId: userId },
			});

			if (!cursorSession) {
				throw new NotFoundError('Cursor session not found');
			}

			queryBuilder.andWhere(
				'(session.lastMessageAt < :lastMessageAt OR (session.lastMessageAt = :lastMessageAt AND session.id > :id))',
				{
					lastMessageAt: cursorSession.lastMessageAt,
					id: cursorSession.id,
				},
			);
		}

		queryBuilder.take(limit);

		return await queryBuilder.getMany();
	}

	async existsById(id: string, userId: string, trx?: EntityManager): Promise<boolean> {
		const em = trx ?? this.manager;
		return await em.exists(ChatHubSession, { where: { id, ownerId: userId } });
	}

	async getOneById(id: string, userId: string, trx?: EntityManager) {
		const em = trx ?? this.manager;
		return await em.findOne(ChatHubSession, {
			where: { id, ownerId: userId },
			relations: {
				messages: true,
				agent: true,
				workflow: {
					activeVersion: true,
				},
			},
		});
	}

	async deleteAll(trx?: EntityManager) {
		const em = trx ?? this.manager;
		return await em.createQueryBuilder().delete().from(ChatHubSession).execute();
	}
}
