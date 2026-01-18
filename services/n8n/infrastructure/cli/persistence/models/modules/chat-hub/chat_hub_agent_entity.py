"""
MIGRATION-META:
  source_path: packages/cli/src/modules/chat-hub/chat-hub-agent.entity.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/modules/chat-hub 的模块。导入/依赖:外部:无；内部:@n8n/api-types、@n8n/db、@n8n/typeorm、n8n-workflow；本地:无。导出:IChatHubAgent、ChatHubAgent。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/chat-hub/chat-hub-agent.entity.ts -> services/n8n/infrastructure/cli/persistence/models/modules/chat-hub/chat_hub_agent_entity.py

import { ChatHubLLMProvider, AgentIconOrEmoji } from '@n8n/api-types';
import { User, CredentialsEntity, JsonColumn, WithTimestamps } from '@n8n/db';
import { Column, Entity, ManyToOne, JoinColumn, PrimaryGeneratedColumn } from '@n8n/typeorm';
import { INode } from 'n8n-workflow';

export interface IChatHubAgent {
	id: string;
	createdAt: Date;
	updatedAt: Date;
	name: string;
	description: string | null;
	icon: AgentIconOrEmoji | null;
	systemPrompt: string;
	ownerId: string;
	credentialId: string | null;
	provider: ChatHubLLMProvider;
	model: string;
	tools: INode[];
}

@Entity({ name: 'chat_hub_agents' })
export class ChatHubAgent extends WithTimestamps {
	@PrimaryGeneratedColumn('uuid')
	id: string;

	/**
	 * The name of the chat agent.
	 */
	@Column({ type: 'varchar', length: 128 })
	name: string;

	/**
	 * The description of the chat agent (optional).
	 */
	@Column({ type: 'varchar', length: 512, nullable: true })
	description: string | null;

	/**
	 * The icon or emoji for the chat agent.
	 */
	@JsonColumn({ nullable: true })
	icon: AgentIconOrEmoji | null;

	/**
	 * The system prompt for the chat agent.
	 */
	@Column({ type: 'text' })
	systemPrompt: string;

	/**
	 * ID of the user that owns this chat agent.
	 */
	@Column({ type: String })
	ownerId: string;

	/**
	 * The user that owns this chat agent.
	 */
	@ManyToOne('User', { onDelete: 'CASCADE' })
	@JoinColumn({ name: 'ownerId' })
	owner?: User;

	/*
	 * ID of the selected credential to use by default with the selected LLM provider.
	 */
	@Column({ type: 'varchar', length: 36, nullable: true })
	credentialId: string | null;

	/**
	 * The selected credential to use by default with the selected LLM provider.
	 */
	@ManyToOne('CredentialsEntity', { onDelete: 'SET NULL', nullable: true })
	@JoinColumn({ name: 'credentialId' })
	credential?: CredentialsEntity | null;

	/*
	 * Enum value of the LLM provider to use, e.g. 'openai', 'anthropic', 'google'.
	 */
	@Column({ type: 'varchar', length: 16, nullable: true })
	provider: ChatHubLLMProvider;

	/*
	 * LLM model to use from the provider (if applicable)
	 */
	@Column({ type: 'varchar', length: 64, nullable: true })
	model: string;

	/**
	 * The tools available to the agent as JSON `INode` definitions.
	 */
	@JsonColumn({ default: '[]' })
	tools: INode[];
}
