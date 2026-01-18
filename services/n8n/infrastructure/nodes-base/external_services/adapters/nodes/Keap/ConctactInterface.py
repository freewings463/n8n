"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Keap/ConctactInterface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Keap 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:IAddress、ICustomField、IEmailContact、IFax、IPhone、ISocialAccount、IContact。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Keap/ConctactInterface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Keap/ConctactInterface.py

import type { IDataObject } from 'n8n-workflow';

export interface IAddress {
	country_code?: string;
	field?: string;
	line1?: string;
	line2?: string;
	locality?: string;
	postal_code?: string;
	region?: string;
	zip_code?: string;
	zip_four?: string;
}

export interface ICustomField {
	content: IDataObject;
	id: number;
}

export interface IEmailContact {
	email?: string;
	field?: string;
}

export interface IFax {
	field?: string;
	number?: string;
	type?: string;
}

export interface IPhone {
	extension?: string;
	field?: string;
	number?: string;
	type?: string;
}

export interface ISocialAccount {
	name?: string;
	type?: string;
}

export interface IContact {
	addresses?: IAddress[];
	anniversary?: string;
	company?: IDataObject;
	contact_type?: string;
	custom_fields?: ICustomField[];
	duplicate_option?: string;
	email_addresses?: IEmailContact[];
	family_name?: string;
	fax_numbers?: IFax[];
	given_name?: string;
	job_title?: string;
	lead_source_id?: number;
	middle_name?: string;
	opt_in_reason?: string;
	origin?: IDataObject;
	owner_id?: number;
	phone_numbers?: IPhone[];
	preferred_locale?: string;
	preferred_name?: string;
	prefix?: string;
	social_accounts?: ISocialAccount[];
	source_type?: string;
	spouse_name?: string;
	suffix?: string;
	time_zone?: string;
	website?: string;
}
