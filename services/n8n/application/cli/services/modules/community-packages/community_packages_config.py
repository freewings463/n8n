"""
MIGRATION-META:
  source_path: packages/cli/src/modules/community-packages/community-packages.config.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/community-packages 的配置。导入/依赖:外部:无；内部:@n8n/config；本地:无。导出:CommunityPackagesConfig。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/community-packages/community-packages.config.ts -> services/n8n/application/cli/services/modules/community-packages/community_packages_config.py

import { Config, Env } from '@n8n/config';

@Config
export class CommunityPackagesConfig {
	/** Whether to enable community packages */
	@Env('N8N_COMMUNITY_PACKAGES_ENABLED')
	enabled: boolean = true;

	/** NPM registry URL to pull community packages from */
	@Env('N8N_COMMUNITY_PACKAGES_REGISTRY')
	registry: string = 'https://registry.npmjs.org';

	/** Whether to reinstall any missing community packages */
	@Env('N8N_REINSTALL_MISSING_PACKAGES')
	reinstallMissing: boolean = false;

	/** Whether to block installation of not verified packages */
	@Env('N8N_UNVERIFIED_PACKAGES_ENABLED')
	unverifiedEnabled: boolean = true;

	/** Whether to enable and show search suggestion of packages verified by n8n */
	@Env('N8N_VERIFIED_PACKAGES_ENABLED')
	verifiedEnabled: boolean = true;

	/** Whether to load community packages */
	@Env('N8N_COMMUNITY_PACKAGES_PREVENT_LOADING')
	preventLoading: boolean = false;
}
