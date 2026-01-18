"""
MIGRATION-META:
  source_path: packages/@n8n/backend-common/src/modules/modules.config.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/backend-common/src/modules 的配置。导入/依赖:外部:无；内部:@n8n/config；本地:./errors/unknown-module.error。导出:MODULE_NAMES、ModuleName、ModulesConfig。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/backend-common treated as infrastructure configuration/runtime environment
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/backend-common/src/modules/modules.config.ts -> services/n8n/infrastructure/n8n-backend-common/configuration/modules/modules_config.py

import { CommaSeparatedStringArray, Config, Env } from '@n8n/config';

import { UnknownModuleError } from './errors/unknown-module.error';

export const MODULE_NAMES = [
	'insights',
	'external-secrets',
	'community-packages',
	'data-table',
	'mcp',
	'provisioning',
	'breaking-changes',
	'source-control',
	'dynamic-credentials',
	'chat-hub',
] as const;

export type ModuleName = (typeof MODULE_NAMES)[number];

class ModuleArray extends CommaSeparatedStringArray<ModuleName> {
	constructor(str: string) {
		super(str);

		for (const moduleName of this) {
			if (!MODULE_NAMES.includes(moduleName)) throw new UnknownModuleError(moduleName);
		}
	}
}

@Config
export class ModulesConfig {
	/** Comma-separated list of all enabled modules. */
	@Env('N8N_ENABLED_MODULES')
	enabledModules: ModuleArray = [];

	/** Comma-separated list of all disabled modules. */
	@Env('N8N_DISABLED_MODULES')
	disabledModules: ModuleArray = [];
}
