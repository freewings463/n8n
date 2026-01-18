"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Aws/Cognito/helpers/constants.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Aws/Cognito 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:HeaderConstants、ERROR_MESSAGES。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Aws/Cognito/helpers/constants.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Aws/Cognito/helpers/constants.py

export const HeaderConstants = {
	AUTHORIZATION: 'authorization',
	X_MS_CONTINUATION: 'x-ms-continuation',
	X_MS_COSMOS_OFFER_AUTOPILOT_SETTING: 'x-ms-cosmos-offer-autopilot-setting',
	X_MS_DOCUMENTDB_IS_UPSERT: 'x-ms-documentdb-is-upsert',
	X_MS_DOCUMENTDB_PARTITIONKEY: 'x-ms-documentdb-partitionkey',
	X_MS_MAX_ITEM_COUNT: 'x-ms-max-item-count',
	X_MS_OFFER_THROUGHPUT: 'x-ms-offer-throughput',
};

export const ERROR_MESSAGES = {
	ResourceNotFound: {
		Group: {
			delete: {
				message: 'The group you are trying to delete could not be found.',
				description: 'Adjust the "Group" parameter setting to delete the group correctly.',
			},
			get: {
				message: 'The group you are trying to retrieve could not be found.',
				description: 'Adjust the "Group" parameter setting to retrieve the group correctly.',
			},
			update: {
				message: 'The group you are trying to update could not be found.',
				description: 'Adjust the "Group" parameter setting to update the group correctly.',
			},
		},
		User: {
			delete: {
				message: 'The user are trying to retrieve could not be found.',
				description: 'Adjust the "User" parameter setting to delete the user correctly.',
			},
			get: {
				message: 'The user you are trying to retrieve could not be found.',
				description: 'Adjust the "User" parameter setting to retrieve the user correctly.',
			},
			update: {
				message: 'The user you are trying to update could not be found.',
				description: 'Adjust the "User" parameter setting to update the user correctly.',
			},
		},
	},
	EntityAlreadyExists: {
		Group: {
			message: 'The group you are trying to create already exists.',
			description: 'Adjust the "Group Name" parameter setting to create the group correctly.',
		},
		User: {
			message: 'The user you are trying to create already exists.',
			description: 'Adjust the "User Name" parameter setting to create the user correctly.',
		},
	},
	UserGroup: {
		add: {
			message: 'The user/group you are trying to add could not be found.',
			description:
				'Adjust the "User" and "Group" parameters to add the user to the group correctly.',
		},
		remove: {
			message: 'The user/group you are trying to remove could not be found.',
			description:
				'Adjust the "User" and "Group" parameters to remove the user from the group correctly.',
		},
	},
};
