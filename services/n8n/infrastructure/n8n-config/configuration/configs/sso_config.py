"""
MIGRATION-META:
  source_path: packages/@n8n/config/src/configs/sso.config.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/config/src/configs 的SSO配置。导入/依赖:外部:无；内部:无；本地:../decorators。导出:SsoConfig。关键函数/方法:无。用于集中定义SSO配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/config treated as infrastructure configuration/runtime environment
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/config/src/configs/sso.config.ts -> services/n8n/infrastructure/n8n-config/configuration/configs/sso_config.py

import { Config, Env, Nested } from '../decorators';

@Config
class SamlConfig {
	/** Whether to enable SAML SSO. */
	@Env('N8N_SSO_SAML_LOGIN_ENABLED')
	loginEnabled: boolean = false;

	@Env('N8N_SSO_SAML_LOGIN_LABEL')
	loginLabel: string = '';
}

@Config
class OidcConfig {
	/** Whether to enable OIDC SSO. */
	@Env('N8N_SSO_OIDC_LOGIN_ENABLED')
	loginEnabled: boolean = false;
}

@Config
class LdapConfig {
	/** Whether to enable LDAP SSO. */
	@Env('N8N_SSO_LDAP_LOGIN_ENABLED')
	loginEnabled: boolean = false;

	@Env('N8N_SSO_LDAP_LOGIN_LABEL')
	loginLabel: string = '';
}

@Config
class ProvisioningConfig {
	/** Whether to provision the instance role from an SSO auth claim */
	@Env('N8N_SSO_SCOPES_PROVISION_INSTANCE_ROLE')
	scopesProvisionInstanceRole: boolean = false;

	/** Whether to provision the project <> role mappings from an SSO auth claim */
	@Env('N8N_SSO_SCOPES_PROVISION_PROJECT_ROLES')
	scopesProvisionProjectRoles: boolean = false;

	/** The name of scope to request on oauth flows */
	@Env('N8N_SSO_SCOPES_NAME')
	scopesName: string = 'n8n';

	/** The name of the expected claim to be returned for provisioning instance role */
	@Env('N8N_SSO_SCOPES_INSTANCE_ROLE_CLAIM_NAME')
	scopesInstanceRoleClaimName: string = 'n8n_instance_role';

	/** The name of the expected claim to be returned for provisioning project <> role mappings */
	@Env('N8N_SSO_SCOPES_PROJECTS_ROLES_CLAIM_NAME')
	scopesProjectsRolesClaimName: string = 'n8n_projects';
}

@Config
export class SsoConfig {
	/** Whether to create users when they log in via SSO. */
	@Env('N8N_SSO_JUST_IN_TIME_PROVISIONING')
	justInTimeProvisioning: boolean = true;

	/** Whether to redirect users from the login dialog to initialize SSO flow. */
	@Env('N8N_SSO_REDIRECT_LOGIN_TO_SSO')
	redirectLoginToSso: boolean = true;

	@Nested
	saml: SamlConfig;

	@Nested
	oidc: OidcConfig;

	@Nested
	ldap: LdapConfig;

	@Nested
	provisioning: ProvisioningConfig;
}
