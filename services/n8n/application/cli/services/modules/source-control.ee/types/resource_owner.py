"""
MIGRATION-META:
  source_path: packages/cli/src/modules/source-control.ee/types/resource-owner.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/source-control.ee/types 的类型。导入/依赖:外部:无；内部:无；本地:无。导出:PersonalResourceOwner、TeamResourceOwner、RemoteResourceOwner、StatusResourceOwner。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。注释目标:When the owner is a personal, it represents the personal project that owns the resource.。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/source-control.ee/types/resource-owner.ts -> services/n8n/application/cli/services/modules/source-control.ee/types/resource_owner.py

/**
 * When the owner is a personal, it represents the personal project that owns the resource.
 */
export type PersonalResourceOwner = {
	type: 'personal';
	/**
	 * The personal project id
	 */
	projectId?: string; // Optional for retrocompatibility
	/**
	 * The personal project name (usually the user name)
	 */
	projectName?: string; // Optional for retrocompatibility
	personalEmail: string;
};

/**
 * When the owner is a team, it represents the team project that owns the resource.
 */
export type TeamResourceOwner = {
	type: 'team';
	/**
	 * The team project id
	 */
	teamId: string;
	/**
	 * The team project name
	 */
	teamName: string;
};

/**
 * When the owner is a string, it represents the personal email of the user who owns the resource.
 */
export type RemoteResourceOwner = string | PersonalResourceOwner | TeamResourceOwner;

export type StatusResourceOwner = {
	type: 'personal' | 'team';
	projectId: string;
	projectName: string;
};
