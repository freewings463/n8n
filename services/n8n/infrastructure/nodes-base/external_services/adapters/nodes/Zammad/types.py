"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Zammad/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Zammad 的类型。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:Resource、AuthMethod、Credentials、BasicAuthCredentials、TokenAuthCredentials、UserAdditionalFields、UserUpdateFields、UserFilterFields 等10项。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Zammad/types.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Zammad/types.py

import type { IDataObject } from 'n8n-workflow';

export declare namespace Zammad {
	export type Resource = 'group' | 'organization' | 'ticket' | 'user';

	export type AuthMethod = 'basicAuth' | 'tokenAuth';

	export type Credentials = BasicAuthCredentials | TokenAuthCredentials;

	type CredentialsBase = {
		baseUrl: string;
		allowUnauthorizedCerts: boolean;
	};

	export type BasicAuthCredentials = CredentialsBase & {
		authType: 'basicAuth';
		username: string;
		password: string;
	};

	export type TokenAuthCredentials = CredentialsBase & {
		authType: 'tokenAuth';
		accessToken: string;
	};

	export type UserAdditionalFields = IDataObject & CustomFieldsUi & AddressUi;
	export type UserUpdateFields = UserAdditionalFields;
	export type UserFilterFields = IDataObject & SortUi;

	export type Organization = {
		active: boolean;
		id: number;
		name: string;
	};

	export type Group = Organization;

	export type GroupUpdateFields = UserUpdateFields;

	export type User = {
		id: number;
		login: string;
		lastname: string;
		email: string;
		role_ids: number[];
	};

	export type Field = {
		id: number;
		display: string;
		name: string;
		object: string;
		created_by_id: number;
	};

	export type UserField = {
		display: string;
		name: string;
	};

	export type CustomFieldsUi = {
		customFieldsUi?: {
			customFieldPairs: Array<{ name: string; value: string }>;
		};
	};

	export type SortUi = {
		sortUi?: {
			sortDetails: {
				sort_by: string;
				order_by: string;
			};
		};
	};

	export type AddressUi = {
		addressUi?: {
			addressDetails: {
				city: string;
				country: string;
				street: string;
				zip: string;
			};
		};
	};

	export type Article = {
		articleDetails: {
			visibility: 'external' | 'internal';
			subject: string;
			body: string;
			sender: 'Agent' | 'Customer' | 'System';
			type: 'chat' | 'email' | 'fax' | 'note' | 'phone' | 'sms';
			reply_to: string;
		};
	};
}
