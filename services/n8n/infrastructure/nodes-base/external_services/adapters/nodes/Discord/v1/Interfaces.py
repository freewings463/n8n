"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Discord/v1/Interfaces.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Discord/v1 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:DiscordWebhook、DiscordAttachment。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Discord/v1/Interfaces.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Discord/v1/Interfaces.py

export interface DiscordWebhook {
	content?: string;
	username?: string;
	avatar_url?: string;
	tts?: boolean;
	file?: Buffer;
	embeds?: any[];
	allowed_mentions?: {
		parse: Array<'roles' | 'users' | 'everyone'>;
		roles: string[];
		users: string[];
		replied_user: boolean;
	};
	flags?: number;
	attachments?: DiscordAttachment[];
	components?: any[];
	payload_json?: any;
}

export interface DiscordAttachment {
	id?: string;
	filename?: string;
	size?: number;
	description?: string;
	content_type?: string;
	url?: string;
	proxy_url?: string;
	height?: number;
	width?: number;
	ephemeral?: boolean;
}
