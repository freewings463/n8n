"""
MIGRATION-META:
  source_path: packages/cli/src/sso.ee/sso-helpers.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/sso.ee 的SSO工具。导入/依赖:外部:无；内部:@n8n/config、@n8n/db 等3项；本地:无。导出:getCurrentAuthenticationMethod、isSamlCurrentAuthenticationMethod、isLdapCurrentAuthenticationMethod、isOidcCurrentAuthenticationMethod 等4项。关键函数/方法:setCurrentAuthenticationMethod、reloadAuthenticationMethod、getCurrentAuthenticationMethod、isSamlCurrentAuthenticationMethod 等6项。用于提供SSO通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - SSO integration orchestration -> application/services/sso
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/sso.ee/sso-helpers.ts -> services/n8n/application/cli/services/sso/sso_helpers.py

import { GlobalConfig } from '@n8n/config';
import { isAuthProviderType, SettingsRepository, type AuthProviderType } from '@n8n/db';
import { Container } from '@n8n/di';

import config from '@/config';
import { Logger } from '@n8n/backend-common';

/**
 * Only one authentication method can be active at a time. This function sets
 * the current authentication method and saves it to the database.
 * SSO methods should only switch to email and then to another method. Email
 * can switch to any method.
 */
export async function setCurrentAuthenticationMethod(
	authenticationMethod: AuthProviderType,
): Promise<void> {
	config.set('userManagement.authenticationMethod', authenticationMethod);
	await Container.get(SettingsRepository).save(
		{
			key: 'userManagement.authenticationMethod',
			value: authenticationMethod,
			loadOnStartup: true,
		},
		{ transaction: false },
	);
}

export async function reloadAuthenticationMethod(): Promise<void> {
	const settings = await Container.get(SettingsRepository).findByKey(
		'userManagement.authenticationMethod',
	);
	if (settings) {
		if (isAuthProviderType(settings.value)) {
			const authenticationMethod = settings.value;
			config.set('userManagement.authenticationMethod', authenticationMethod);
			Container.get(Logger).debug('Reloaded authentication method from the database', {
				authenticationMethod,
			});
		} else {
			Container.get(Logger).warn('Invalid authentication method read from the database', {
				value: settings.value,
			});
		}
	}
}

export function getCurrentAuthenticationMethod(): AuthProviderType {
	return config.getEnv('userManagement.authenticationMethod');
}

export function isSamlCurrentAuthenticationMethod(): boolean {
	return getCurrentAuthenticationMethod() === 'saml';
}

export function isLdapCurrentAuthenticationMethod(): boolean {
	return getCurrentAuthenticationMethod() === 'ldap';
}

export function isOidcCurrentAuthenticationMethod(): boolean {
	return getCurrentAuthenticationMethod() === 'oidc';
}

export function isSsoCurrentAuthenticationMethod(): boolean {
	return (
		isSamlCurrentAuthenticationMethod() ||
		isLdapCurrentAuthenticationMethod() ||
		isOidcCurrentAuthenticationMethod()
	);
}

export function isEmailCurrentAuthenticationMethod(): boolean {
	return getCurrentAuthenticationMethod() === 'email';
}

export function isSsoJustInTimeProvisioningEnabled(): boolean {
	return Container.get(GlobalConfig).sso.justInTimeProvisioning;
}

export function doRedirectUsersFromLoginToSsoFlow(): boolean {
	return Container.get(GlobalConfig).sso.redirectLoginToSso;
}
