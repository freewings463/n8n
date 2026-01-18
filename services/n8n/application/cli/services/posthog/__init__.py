"""
MIGRATION-META:
  source_path: packages/cli/src/posthog/index.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/posthog 的入口。导入/依赖:外部:posthog-node；内部:@n8n/config、@n8n/db、@n8n/di、n8n-core、n8n-workflow；本地:无。导出:PostHogClient。关键函数/方法:init、stop、track、getFeatureFlags。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/posthog/index.ts -> services/n8n/application/cli/services/posthog/__init__.py

import { GlobalConfig } from '@n8n/config';
import type { PublicUser } from '@n8n/db';
import { Service } from '@n8n/di';
import { InstanceSettings } from 'n8n-core';
import type { FeatureFlags, ITelemetryTrackProperties } from 'n8n-workflow';
import type { PostHog } from 'posthog-node';

@Service()
export class PostHogClient {
	private postHog?: PostHog;

	constructor(
		private readonly instanceSettings: InstanceSettings,
		private readonly globalConfig: GlobalConfig,
	) {}

	async init() {
		const { enabled, posthogConfig } = this.globalConfig.diagnostics;
		if (!enabled) {
			return;
		}

		const { PostHog } = await import('posthog-node');
		this.postHog = new PostHog(posthogConfig.apiKey, {
			host: posthogConfig.apiHost,
		});
	}

	async stop(): Promise<void> {
		if (this.postHog) {
			return this.postHog.shutdown();
		}
	}

	track(payload: { userId: string; event: string; properties: ITelemetryTrackProperties }): void {
		this.postHog?.capture({
			distinctId: payload.userId,
			sendFeatureFlags: true,
			...payload,
		});
	}

	async getFeatureFlags(user: Pick<PublicUser, 'id' | 'createdAt'>): Promise<FeatureFlags> {
		if (!this.postHog) return {};

		const fullId = [this.instanceSettings.instanceId, user.id].join('#');

		// cannot use local evaluation because that requires PostHog personal api key with org-wide
		// https://github.com/PostHog/posthog/issues/4849
		return await this.postHog.getAllFlags(fullId, {
			personProperties: {
				created_at_timestamp: user.createdAt.getTime().toString(),
			},
		});
	}
}
