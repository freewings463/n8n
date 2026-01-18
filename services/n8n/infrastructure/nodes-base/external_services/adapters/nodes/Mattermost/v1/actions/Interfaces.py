"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Mattermost/v1/actions/Interfaces.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Mattermost/v1 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:Mattermost、MattermostChannel、MattermostMessage、MattermostReaction、MattermostUser、ChannelProperties、MessageProperties、ReactionProperties 等2项。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Mattermost/v1/actions/Interfaces.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Mattermost/v1/actions/Interfaces.py

import type { AllEntities, Entity, PropertiesOf } from 'n8n-workflow';

type MattermostMap = {
	channel: 'addUser' | 'create' | 'delete' | 'members' | 'restore' | 'statistics' | 'search';
	message: 'delete' | 'post' | 'postEphemeral';
	reaction: 'create' | 'delete' | 'getAll';
	user: 'create' | 'deactive' | 'getAll' | 'getByEmail' | 'getById' | 'invite';
};

export type Mattermost = AllEntities<MattermostMap>;

export type MattermostChannel = Entity<MattermostMap, 'channel'>;
export type MattermostMessage = Entity<MattermostMap, 'message'>;
export type MattermostReaction = Entity<MattermostMap, 'reaction'>;
export type MattermostUser = Entity<MattermostMap, 'user'>;

export type ChannelProperties = PropertiesOf<MattermostChannel>;
export type MessageProperties = PropertiesOf<MattermostMessage>;
export type ReactionProperties = PropertiesOf<MattermostReaction>;
export type UserProperties = PropertiesOf<MattermostUser>;

export interface IAttachment {
	fields: {
		item?: object[];
	};
	actions: {
		item?: object[];
	};
}
