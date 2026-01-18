"""
MIGRATION-META:
  source_path: packages/cli/src/config/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/config 的入口。导入/依赖:外部:convict；内部:@n8n/backend-common、@n8n/config、@n8n/di、n8n-workflow、@/constants；本地:./schema。导出:Config。关键函数/方法:setGlobalState。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected runtime IO/external interaction -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/config/index.ts -> services/n8n/infrastructure/cli/container/config/__init__.py

import { inTest } from '@n8n/backend-common';
import { GlobalConfig } from '@n8n/config';
import { Container } from '@n8n/di';
import convict from 'convict';
import { readFileSync } from 'fs';
import { setGlobalState, UserError } from 'n8n-workflow';

import { inE2ETests } from '@/constants';

const globalConfig = Container.get(GlobalConfig);

if (inE2ETests) {
	globalConfig.diagnostics.enabled = false;
	globalConfig.publicApi.disabled = true;
	process.env.EXTERNAL_FRONTEND_HOOKS_URLS = '';
	process.env.N8N_PERSONALIZATION_ENABLED = 'false';
	process.env.N8N_AI_ENABLED = 'true';
} else if (inTest) {
	globalConfig.logging.level = 'silent';
	globalConfig.publicApi.disabled = true;
	process.env.SKIP_STATISTICS_EVENTS = 'true';
	globalConfig.auth.cookie.secure = false;
	process.env.N8N_SKIP_AUTH_ON_OAUTH_CALLBACK = 'false';
}

// Load schema after process.env has been overwritten
import { schema } from './schema';
const config = convict(schema, { args: [] });

// eslint-disable-next-line @typescript-eslint/unbound-method
config.getEnv = config.get;

// Load overwrites when not in tests
if (!inE2ETests && !inTest) {
	// Overwrite config from files defined in "_FILE" environment variables
	Object.entries(process.env).forEach(([envName, fileName]) => {
		if (envName.endsWith('_FILE') && fileName) {
			const configEnvName = envName.replace(/_FILE$/, '');
			// @ts-ignore
			// eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
			const key = config._env[configEnvName]?.[0] as string;
			if (key) {
				let value: string;
				try {
					value = readFileSync(fileName, 'utf8');
				} catch (error) {
					// eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
					if (error.code === 'ENOENT') {
						throw new UserError('File not found', { extra: { fileName } });
					}
					throw error;
				}
				config.set(key, value);
			}
		}
	});
}

setGlobalState({
	defaultTimezone: globalConfig.generic.timezone,
});

// eslint-disable-next-line import-x/no-default-export
export default config;

export type Config = typeof config;
