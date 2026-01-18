"""
MIGRATION-META:
  source_path: packages/@n8n/config/src/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/config/src 的入口。导入/依赖:外部:zod；内部:无；本地:./configs/ai-assistant.config、./configs/ai-builder.config、./configs/ai.config、./configs/auth.config 等34项。再导出:./custom-types。导出:Config、Env、Nested、AiConfig、DatabaseConfig、SqliteConfig、InstanceSettingsConfig、TaskRunnersConfig 等13项。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/config treated as infrastructure configuration/runtime environment
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/config/src/index.ts -> services/n8n/infrastructure/n8n-config/configuration/__init__.py

import { z } from 'zod';

import { AiAssistantConfig } from './configs/ai-assistant.config';
import { AiBuilderConfig } from './configs/ai-builder.config';
import { AiConfig } from './configs/ai.config';
import { AuthConfig } from './configs/auth.config';
import { CacheConfig } from './configs/cache.config';
import { CredentialsConfig } from './configs/credentials.config';
import { DataTableConfig } from './configs/data-table.config';
import { DatabaseConfig } from './configs/database.config';
import { DeploymentConfig } from './configs/deployment.config';
import { DiagnosticsConfig } from './configs/diagnostics.config';
import { DynamicBannersConfig } from './configs/dynamic-banners.config';
import { EndpointsConfig } from './configs/endpoints.config';
import { EventBusConfig } from './configs/event-bus.config';
import { ExecutionsConfig } from './configs/executions.config';
import { ExternalHooksConfig } from './configs/external-hooks.config';
import { GenericConfig } from './configs/generic.config';
import { HiringBannerConfig } from './configs/hiring-banner.config';
import { LicenseConfig } from './configs/license.config';
import { LoggingConfig } from './configs/logging.config';
import { MfaConfig } from './configs/mfa.config';
import { MultiMainSetupConfig } from './configs/multi-main-setup.config';
import { NodesConfig } from './configs/nodes.config';
import { PersonalizationConfig } from './configs/personalization.config';
import { PublicApiConfig } from './configs/public-api.config';
import { RedisConfig } from './configs/redis.config';
import { TaskRunnersConfig } from './configs/runners.config';
import { ScalingModeConfig } from './configs/scaling-mode.config';
import { SecurityConfig } from './configs/security.config';
import { SentryConfig } from './configs/sentry.config';
import { SsoConfig } from './configs/sso.config';
import { TagsConfig } from './configs/tags.config';
import { TemplatesConfig } from './configs/templates.config';
import { UserManagementConfig } from './configs/user-management.config';
import { VersionNotificationsConfig } from './configs/version-notifications.config';
import { WorkflowHistoryCompactionConfig } from './configs/workflow-history-compaction.config';
import { WorkflowHistoryConfig } from './configs/workflow-history.config';
import { WorkflowsConfig } from './configs/workflows.config';
import { Config, Env, Nested } from './decorators';

export { Config, Env, Nested } from './decorators';
export { AiConfig } from './configs/ai.config';
export { DatabaseConfig, SqliteConfig } from './configs/database.config';
export { InstanceSettingsConfig } from './configs/instance-settings-config';
export type { TaskRunnerMode } from './configs/runners.config';
export { TaskRunnersConfig } from './configs/runners.config';
export { SecurityConfig } from './configs/security.config';
export { ExecutionsConfig } from './configs/executions.config';
export { LOG_SCOPES } from './configs/logging.config';
export type { LogScope } from './configs/logging.config';
export { WorkflowsConfig } from './configs/workflows.config';
export * from './custom-types';
export { DeploymentConfig } from './configs/deployment.config';
export { MfaConfig } from './configs/mfa.config';
export { HiringBannerConfig } from './configs/hiring-banner.config';
export { PersonalizationConfig } from './configs/personalization.config';
export { NodesConfig } from './configs/nodes.config';
export { CronLoggingConfig } from './configs/logging.config';
export { WorkflowHistoryCompactionConfig } from './configs/workflow-history-compaction.config';

const protocolSchema = z.enum(['http', 'https']);

export type Protocol = z.infer<typeof protocolSchema>;

@Config
export class GlobalConfig {
	@Nested
	auth: AuthConfig;

	@Nested
	database: DatabaseConfig;

	@Nested
	credentials: CredentialsConfig;

	@Nested
	userManagement: UserManagementConfig;

	@Nested
	versionNotifications: VersionNotificationsConfig;

	@Nested
	dynamicBanners: DynamicBannersConfig;

	@Nested
	publicApi: PublicApiConfig;

	@Nested
	externalHooks: ExternalHooksConfig;

	@Nested
	templates: TemplatesConfig;

	@Nested
	eventBus: EventBusConfig;

	@Nested
	nodes: NodesConfig;

	@Nested
	workflows: WorkflowsConfig;

	@Nested
	sentry: SentryConfig;

	/** Path n8n is deployed to */
	@Env('N8N_PATH')
	path: string = '/';

	/** Host name n8n can be reached */
	@Env('N8N_HOST')
	host: string = 'localhost';

	/** HTTP port n8n can be reached */
	@Env('N8N_PORT')
	port: number = 5678;

	/** IP address n8n should listen on */
	@Env('N8N_LISTEN_ADDRESS')
	listen_address: string = '::';

	/** HTTP Protocol via which n8n can be reached */
	@Env('N8N_PROTOCOL', protocolSchema)
	protocol: Protocol = 'http';

	@Nested
	endpoints: EndpointsConfig;

	@Nested
	cache: CacheConfig;

	@Nested
	queue: ScalingModeConfig;

	@Nested
	logging: LoggingConfig;

	@Nested
	taskRunners: TaskRunnersConfig;

	@Nested
	multiMainSetup: MultiMainSetupConfig;

	@Nested
	generic: GenericConfig;

	@Nested
	license: LicenseConfig;

	@Nested
	security: SecurityConfig;

	@Nested
	executions: ExecutionsConfig;

	@Nested
	diagnostics: DiagnosticsConfig;

	@Nested
	aiAssistant: AiAssistantConfig;

	@Nested
	aiBuilder: AiBuilderConfig;

	@Nested
	tags: TagsConfig;

	@Nested
	workflowHistory: WorkflowHistoryConfig;

	@Nested
	deployment: DeploymentConfig;

	@Nested
	mfa: MfaConfig;

	@Nested
	hiringBanner: HiringBannerConfig;

	@Nested
	personalization: PersonalizationConfig;

	@Nested
	sso: SsoConfig;

	/** Default locale for the UI. */
	@Env('N8N_DEFAULT_LOCALE')
	defaultLocale: string = 'en';

	/** Whether to hide the page that shows active workflows and executions count. */
	@Env('N8N_HIDE_USAGE_PAGE')
	hideUsagePage: boolean = false;

	/** Number of reverse proxies n8n is running behind. */
	@Env('N8N_PROXY_HOPS')
	proxy_hops: number = 0;

	/** SSL key for HTTPS protocol. */
	@Env('N8N_SSL_KEY')
	ssl_key: string = '';

	/** SSL cert for HTTPS protocol. */
	@Env('N8N_SSL_CERT')
	ssl_cert: string = '';

	/** Public URL where the editor is accessible. Also used for emails sent from n8n. */
	@Env('N8N_EDITOR_BASE_URL')
	editorBaseUrl: string = '';

	/** URLs to external frontend hooks files, separated by semicolons. */
	@Env('EXTERNAL_FRONTEND_HOOKS_URLS')
	externalFrontendHooksUrls: string = '';

	@Nested
	redis: RedisConfig;

	@Nested
	ai: AiConfig;

	@Nested
	dataTable: DataTableConfig;

	@Nested
	workflowHistoryCompaction: WorkflowHistoryCompactionConfig;
}
