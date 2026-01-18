"""
MIGRATION-META:
  source_path: packages/cli/src/sso.ee/saml/service-provider.ee.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/sso.ee/saml 的SSO模块。导入/依赖:外部:samlify；内部:@n8n/api-types、@n8n/di、@/services/url.service；本地:无。导出:getServiceProviderEntityId、getServiceProviderReturnUrl、getServiceProviderConfigTestReturnUrl、getServiceProviderInstance。关键函数/方法:getServiceProviderEntityId、getServiceProviderReturnUrl、getServiceProviderConfigTestReturnUrl、getServiceProviderInstance。用于承载SSO实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - SSO integration orchestration -> application/services/sso
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/sso.ee/saml/service-provider.ee.ts -> services/n8n/application/cli/services/sso/saml/service_provider_ee.py

import type { SamlPreferences } from '@n8n/api-types';
import { Container } from '@n8n/di';
import type { ServiceProviderInstance } from 'samlify';

import { UrlService } from '@/services/url.service';

let serviceProviderInstance: ServiceProviderInstance | undefined;

export function getServiceProviderEntityId(): string {
	return Container.get(UrlService).getInstanceBaseUrl() + '/rest/sso/saml/metadata';
}

export function getServiceProviderReturnUrl(): string {
	return Container.get(UrlService).getInstanceBaseUrl() + '/rest/sso/saml/acs';
}

export function getServiceProviderConfigTestReturnUrl(): string {
	// TODO: what is this URL?
	return Container.get(UrlService).getInstanceBaseUrl() + '/config/test/return';
}

// TODO:SAML: make these configurable for the end user
export function getServiceProviderInstance(
	prefs: SamlPreferences,
	// eslint-disable-next-line @typescript-eslint/consistent-type-imports
	samlify: typeof import('samlify'),
): ServiceProviderInstance {
	if (serviceProviderInstance === undefined) {
		serviceProviderInstance = samlify.ServiceProvider({
			entityID: getServiceProviderEntityId(),
			authnRequestsSigned: prefs.authnRequestsSigned,
			wantAssertionsSigned: prefs.wantAssertionsSigned,
			wantMessageSigned: prefs.wantMessageSigned,
			signatureConfig: prefs.signatureConfig,
			relayState: prefs.relayState,
			nameIDFormat: ['urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress'],
			assertionConsumerService: [
				{
					isDefault: prefs.acsBinding === 'post',
					Binding: 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST',
					Location: getServiceProviderReturnUrl(),
				},
				{
					isDefault: prefs.acsBinding === 'redirect',
					Binding: 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-REDIRECT',
					Location: getServiceProviderReturnUrl(),
				},
			],
		});
	}

	return serviceProviderInstance;
}
