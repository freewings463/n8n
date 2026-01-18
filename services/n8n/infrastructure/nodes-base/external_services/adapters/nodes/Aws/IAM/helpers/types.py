"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Aws/IAM/helpers/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Aws/IAM 的类型。导入/依赖:外部:无；内部:无；本地:无。导出:Group、User、Tags、GetUserResponseBody、GetGroupResponseBody、GetAllUsersResponseBody、GetAllGroupsResponseBody、AwsError 等2项。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Aws/IAM/helpers/types.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Aws/IAM/helpers/types.py

export type Group = {
	Arn: string;
	CreateDate: number;
	GroupId: string;
	GroupName: string;
	Path?: string;
};

export type User = {
	Arn: string;
	CreateDate: number;
	PasswordLastUsed?: number;
	Path?: string;
	PermissionsBoundary?: string;
	Tags: Array<{ Key: string; Value: string }>;
	UserId: string;
	UserName: string;
};

export type Tags = {
	tags: Array<{ key: string; value: string }>;
};

export type GetUserResponseBody = {
	GetUserResponse: {
		GetUserResult: {
			User: User;
		};
	};
};

export type GetGroupResponseBody = {
	GetGroupResponse: {
		GetGroupResult: {
			Group: Group;
			Users?: User[];
		};
	};
};

export type GetAllUsersResponseBody = {
	ListUsersResponse: {
		ListUsersResult: {
			Users: User[];
			IsTruncated: boolean;
			Marker: string;
		};
	};
};

export type GetAllGroupsResponseBody = {
	ListGroupsResponse: {
		ListGroupsResult: {
			Groups: Group[];
			IsTruncated: boolean;
			Marker: string;
		};
	};
};

export type AwsError = {
	Code: string;
	Message: string;
};

export type ErrorResponse = {
	Error: {
		Code: string;
		Message: string;
	};
};

export type ErrorMessage = {
	message: string;
	description: string;
};
