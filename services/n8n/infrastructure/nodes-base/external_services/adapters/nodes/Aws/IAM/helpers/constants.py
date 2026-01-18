"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Aws/IAM/helpers/constants.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Aws/IAM 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:CURRENT_VERSION、BASE_URL、ERROR_DESCRIPTIONS。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Aws/IAM/helpers/constants.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Aws/IAM/helpers/constants.py

export const CURRENT_VERSION = '2010-05-08';
export const BASE_URL = 'https://iam.amazonaws.com';
export const ERROR_DESCRIPTIONS = {
	EntityAlreadyExists: {
		User: 'The given user name already exists - try entering a unique name for the user.',
		Group: 'The given group name already exists - try entering a unique name for the group.',
	},
	NoSuchEntity: {
		User: 'The given user was not found - try entering a different user.',
		Group: 'The given group was not found - try entering a different group.',
	},
	DeleteConflict: {
		Default: 'Cannot delete entity, please remove users from group first.',
	},
};
