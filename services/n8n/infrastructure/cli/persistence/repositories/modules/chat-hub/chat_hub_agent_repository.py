"""
MIGRATION-META:
  source_path: packages/cli/src/modules/chat-hub/chat-hub-agent.repository.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/modules/chat-hub 的仓储。导入/依赖:外部:无；内部:@n8n/di、@n8n/typeorm；本地:./chat-hub-agent.entity。导出:ChatHubAgentRepository。关键函数/方法:createAgent、updateAgent、deleteAgent、getManyByUserId、getOneById。用于封装该模块数据读写与查询细节，隔离持久层。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected TypeORM Repository/EntityManager usage
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/chat-hub/chat-hub-agent.repository.ts -> services/n8n/infrastructure/cli/persistence/repositories/modules/chat-hub/chat_hub_agent_repository.py

import { Service } from '@n8n/di';
import { DataSource, EntityManager, Repository } from '@n8n/typeorm';

import { ChatHubAgent, IChatHubAgent } from './chat-hub-agent.entity';

@Service()
export class ChatHubAgentRepository extends Repository<ChatHubAgent> {
	constructor(dataSource: DataSource) {
		super(ChatHubAgent, dataSource.manager);
	}

	async createAgent(
		agent: Partial<IChatHubAgent> & Pick<IChatHubAgent, 'id'>,
		trx?: EntityManager,
	) {
		const em = trx ?? this.manager;
		await em.insert(ChatHubAgent, agent);
		return await em.findOneOrFail(ChatHubAgent, {
			where: { id: agent.id },
		});
	}

	async updateAgent(id: string, updates: Partial<IChatHubAgent>, trx?: EntityManager) {
		const em = trx ?? this.manager;
		await em.update(ChatHubAgent, { id }, updates);
		return await em.findOneOrFail(ChatHubAgent, {
			where: { id },
		});
	}

	async deleteAgent(id: string, trx?: EntityManager) {
		const em = trx ?? this.manager;
		return await em.delete(ChatHubAgent, { id });
	}

	async getManyByUserId(userId: string) {
		return await this.find({
			where: { ownerId: userId },
			order: { createdAt: 'DESC' },
		});
	}

	async getOneById(id: string, userId: string, trx?: EntityManager) {
		const em = trx ?? this.manager;
		return await em.findOne(ChatHubAgent, {
			where: { id, ownerId: userId },
		});
	}
}
