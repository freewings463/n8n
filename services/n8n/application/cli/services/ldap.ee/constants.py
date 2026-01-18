"""
MIGRATION-META:
  source_path: packages/cli/src/ldap.ee/constants.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/ldap.ee 的LDAP模块。导入/依赖:外部:无；内部:@n8n/constants；本地:无。导出:LDAP_LOGIN_LABEL、LDAP_LOGIN_ENABLED、BINARY_AD_ATTRIBUTES、LDAP_CONFIG_SCHEMA、NON_SENSIBLE_LDAP_CONFIG_PROPERTIES。关键函数/方法:无。用于承载LDAP实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/ldap.ee/constants.ts -> services/n8n/application/cli/services/ldap.ee/constants.py

import type { LdapConfig } from '@n8n/constants';

export const LDAP_LOGIN_LABEL = 'sso.ldap.loginLabel';

export const LDAP_LOGIN_ENABLED = 'sso.ldap.loginEnabled';

export const BINARY_AD_ATTRIBUTES = ['objectGUID', 'objectSid'];

export const LDAP_CONFIG_SCHEMA = {
	$schema: 'https://json-schema.org/draft/2019-09/schema',
	type: 'object',
	properties: {
		emailAttribute: {
			type: 'string',
		},
		firstNameAttribute: {
			type: 'string',
		},
		lastNameAttribute: {
			type: 'string',
		},
		ldapIdAttribute: {
			type: 'string',
		},
		loginIdAttribute: {
			type: 'string',
		},
		bindingAdminDn: {
			type: 'string',
		},
		bindingAdminPassword: {
			type: 'string',
		},
		baseDn: {
			type: 'string',
		},
		connectionUrl: {
			type: 'string',
		},
		connectionSecurity: {
			type: 'string',
		},
		connectionPort: {
			type: 'number',
		},
		allowUnauthorizedCerts: {
			type: 'boolean',
		},
		userFilter: {
			type: 'string',
		},
		loginEnabled: {
			type: 'boolean',
		},
		loginLabel: {
			type: 'string',
		},
		synchronizationEnabled: {
			type: 'boolean',
		},
		synchronizationInterval: {
			type: 'number',
		},
		searchPageSize: {
			type: 'number',
		},
		searchTimeout: {
			type: 'number',
		},
		enforceEmailUniqueness: {
			type: 'boolean',
		},
	},
	required: [
		'loginEnabled',
		'loginLabel',
		'connectionUrl',
		'allowUnauthorizedCerts',
		'connectionSecurity',
		'connectionPort',
		'baseDn',
		'bindingAdminDn',
		'bindingAdminPassword',
		'firstNameAttribute',
		'lastNameAttribute',
		'emailAttribute',
		'loginIdAttribute',
		'ldapIdAttribute',
		'userFilter',
		'synchronizationEnabled',
		'synchronizationInterval',
		'searchPageSize',
		'searchTimeout',
	],
	additionalProperties: false,
};

export const NON_SENSIBLE_LDAP_CONFIG_PROPERTIES: Array<keyof LdapConfig> = [
	'loginEnabled',
	'emailAttribute',
	'firstNameAttribute',
	'lastNameAttribute',
	'loginIdAttribute',
	'ldapIdAttribute',
	'synchronizationEnabled',
	'synchronizationInterval',
	'searchPageSize',
	'searchTimeout',
	'loginLabel',
	'enforceEmailUniqueness',
];
