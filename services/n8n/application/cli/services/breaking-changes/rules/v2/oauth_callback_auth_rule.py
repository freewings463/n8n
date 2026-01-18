"""
MIGRATION-META:
  source_path: packages/cli/src/modules/breaking-changes/rules/v2/oauth-callback-auth.rule.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/breaking-changes/rules 的OAuth模块。导入/依赖:外部:无；内部:@n8n/di；本地:../../types。导出:OAuthCallbackAuthRule。关键函数/方法:getMetadata、detect。用于承载OAuth实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/breaking-changes/rules/v2/oauth-callback-auth.rule.ts -> services/n8n/application/cli/services/breaking-changes/rules/v2/oauth_callback_auth_rule.py

import { Service } from '@n8n/di';

import type {
	BreakingChangeRuleMetadata,
	IBreakingChangeInstanceRule,
	InstanceDetectionReport,
} from '../../types';
import { BreakingChangeCategory } from '../../types';

@Service()
export class OAuthCallbackAuthRule implements IBreakingChangeInstanceRule {
	id: string = 'oauth-callback-auth-v2';

	getMetadata(): BreakingChangeRuleMetadata {
		return {
			version: 'v2',
			title: 'Require auth on OAuth callback URLs by default',
			description:
				'OAuth callbacks now enforce n8n user authentication by default for improved security',
			category: BreakingChangeCategory.instance,
			severity: 'medium',
			documentationUrl:
				'https://docs.n8n.io/2-0-breaking-changes/#require-authentication-on-oauth-callback-urls-by-default',
		};
	}

	async detect(): Promise<InstanceDetectionReport> {
		// If the env var is set explicitly, then the instance is not affected
		// because the user has already made a choice
		if (process.env.N8N_SKIP_AUTH_ON_OAUTH_CALLBACK) {
			return { isAffected: false, instanceIssues: [], recommendations: [] };
		}

		return {
			isAffected: true,
			instanceIssues: [
				{
					title: 'OAuth callback authentication now required',
					description:
						'OAuth callbacks will now enforce n8n user authentication by default unless N8N_SKIP_AUTH_ON_OAUTH_CALLBACK is explicitly set to true.',
					level: 'warning',
				},
			],
			recommendations: [
				{
					action: 'Review OAuth workflows',
					description:
						'If you need to skip authentication on OAuth callbacks (e.g., for embed mode), set N8N_SKIP_AUTH_ON_OAUTH_CALLBACK=true',
				},
			],
		};
	}
}
