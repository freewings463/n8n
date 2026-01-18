"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Taiga/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Taiga 的类型。导入/依赖:外部:无；内部:无；本地:无。导出:Resource、Operation、LoadedResource、LoadOption、LoadedUser、LoadedUserStory、LoadedEpic、LoadedTags 等3项。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Taiga/types.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Taiga/types.py

export type Resource = 'epic' | 'issue' | 'task' | 'userStory';

export type Operation = 'create' | 'delete' | 'update' | 'get' | 'getAll';

export type LoadedResource = {
	id: string;
	name: string;
};

export type LoadOption = {
	value: string;
	name: string;
};

export type LoadedUser = {
	id: string;
	full_name_display: string;
};

export type LoadedUserStory = {
	id: string;
	subject: string;
};

export type LoadedEpic = LoadedUserStory;

export type LoadedTags = {
	[tagName: string]: string | null; // hex color
};

export type Operations = 'all' | 'create' | 'delete' | 'change';

export type Resources = 'all' | 'issue' | 'milestone' | 'task' | 'userstory' | 'wikipage';

export type WebhookPayload = {
	action: Operations;
	type: Resources;
	by: Record<string, string | number>;
	date: string;
	data: Record<string, string | number | object | string[]>;
};
