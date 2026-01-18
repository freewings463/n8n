"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ActionNetwork/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ActionNetwork 的类型。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:LanguageOptions、Resource、Operation、LanguageCodes、AllFieldsUi、EmailAddressUi、EmailAddressField、PhoneNumberField 等8项。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ActionNetwork/types.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/ActionNetwork/types.py

import type { INodeProperties } from 'n8n-workflow';

export type LanguageOptions = INodeProperties['options'];

export type Resource =
	| 'attendance'
	| 'event'
	| 'person'
	| 'personTag'
	| 'petition'
	| 'signature'
	| 'tag';

export type Operation = 'create' | 'delete' | 'get' | 'getAll' | 'update' | 'add' | 'remove';

// @ts-ignore
export type LanguageCodes = LanguageOptions[number]['value'];

// ----------------------------------------
//              UI fields
// ----------------------------------------

export type AllFieldsUi = {
	email_addresses: EmailAddressUi;
	postal_addresses: PostalAddressesUi;
	phone_numbers: PhoneNumberUi;
	languages_spoken: LanguageCodes;
	target: string;
	location: LocationUi;
};

export type EmailAddressUi = {
	email_addresses_fields: EmailAddressField;
};

export type EmailAddressField = {
	primary: boolean;
	address: string;
	status: EmailStatus;
};

type BaseStatus = 'subscribed' | 'unsubscribed' | 'bouncing' | 'previous bounce';

type EmailStatus = BaseStatus | 'spam complaint' | 'previous spam complaint';

type PhoneNumberUi = {
	phone_numbers_fields: PhoneNumberField[];
};

export type PhoneNumberField = {
	primary: boolean;
	number: string;
	status: BaseStatus;
};

type PostalAddressesUi = {
	postal_addresses_fields: PostalAddressField[];
};

type LocationUi = {
	postal_addresses_fields: PostalAddressField;
};

export type PostalAddressField = {
	primary: boolean;
	address_lines: string;
	locality: string;
	region: string;
	postal_code: string;
	country: string;
	language: LanguageCodes;
	location: { location_fields: LatitudeLongitude };
};

type LatitudeLongitude = {
	latitude: string;
	longitude: string;
};

export type FieldWithPrimaryField = EmailAddressField | PhoneNumberField | PostalAddressField;

// ----------------------------------------
//                 responses
// ----------------------------------------

export type LinksFieldContainer = { _links: { self: { href: string } } };

export type Response = JsonObject & LinksFieldContainer;

export type PersonResponse = Response & {
	identifiers: string[];
	email_addresses: EmailAddressField[];
	phone_numbers: PhoneNumberField[];
	postal_addresses: PostalAddressField[];
	languages_spoken: LanguageCodes[];
};

export type PetitionResponse = Response & { _embedded: { 'osdi:creator': PersonResponse } };

// ----------------------------------------
//                 utils
// ----------------------------------------

export type JsonValue = string | number | boolean | null | JsonObject | JsonValue[];

export type JsonObject = { [key: string]: JsonValue };
