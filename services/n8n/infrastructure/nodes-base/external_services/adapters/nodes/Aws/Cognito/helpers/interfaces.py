"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Aws/Cognito/helpers/interfaces.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Aws/Cognito 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:IUserAttribute、IUser、IGroup、IListUsersResponse、IListGroupsResponse、IGroupWithUserResponse、IUserAttributeInput、IUserPool 等3项。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Aws/Cognito/helpers/interfaces.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Aws/Cognito/helpers/interfaces.py

import type { IDataObject } from 'n8n-workflow';

export interface IUserAttribute {
	Name: string;
	Value: string;
}

export interface IUser {
	Username: string;
	Enabled: boolean;
	UserCreateDate: string;
	UserLastModifiedDate: string;
	UserStatus: string;
	Attributes?: IUserAttribute[];
}

export interface IGroup {
	GroupName: string;
}

export interface IListUsersResponse {
	Users: IUser[];
	NextToken?: string;
}

export interface IListGroupsResponse {
	Groups: IGroup[];
	NextToken?: string;
}

export interface IGroupWithUserResponse extends IGroup {
	Users: IUser[];
}

export interface IUserAttributeInput {
	attributeType: string;
	standardName: string;
	customName: string;
	value: string;
}

export interface IUserPool {
	Id: string;
	Name: string;
	UsernameAttributes?: string[];
	AccountRecoverySetting?: IDataObject;
	AdminCreateUserConfig?: IDataObject;
	EmailConfiguration?: IDataObject;
	LambdaConfig?: IDataObject;
	Policies?: IDataObject;
	SchemaAttributes?: IDataObject;
	UserAttributeUpdateSettings?: IDataObject;
	UserPoolTags?: IDataObject;
	UserPoolTier?: string;
	VerificationMessageTemplate?: IDataObject;
}

export interface Filters {
	filter?: {
		attribute?: string;
		value?: string;
	};
}

export interface AwsError {
	__type?: string;
	message?: string;
}

export interface ErrorMessage {
	message: string;
	description: string;
}
