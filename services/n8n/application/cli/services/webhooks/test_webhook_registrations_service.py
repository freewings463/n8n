"""
MIGRATION-META:
  source_path: packages/cli/src/webhooks/test-webhook-registrations.service.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/webhooks 的Webhook服务。导入/依赖:外部:无；内部:@n8n/di、n8n-core、@/constants、@/services/…/cache.service、@n8n/backend-common；本地:无。导出:TestWebhookRegistration、TestWebhookRegistrationsService。关键函数/方法:register、get、isTestWebhookRegistration、deregister、getAllKeys、getAllRegistrations、getRegistrationsHash、toKey。用于封装Webhook业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/webhooks/test-webhook-registrations.service.ts -> services/n8n/application/cli/services/webhooks/test_webhook_registrations_service.py

import { Service } from '@n8n/di';
import { InstanceSettings } from 'n8n-core';
import {
	type IWebhookData,
	type IWorkflowBase,
	type IDestinationNode,
	UserError,
} from 'n8n-workflow';

import { TEST_WEBHOOK_TIMEOUT, TEST_WEBHOOK_TIMEOUT_BUFFER } from '@/constants';
import { CacheService } from '@/services/cache/cache.service';
import { isObjectLiteral } from '@n8n/backend-common';

const TEST_WEBHOOK_REGISTRATION_VERSION = 1;

export type TestWebhookRegistration = {
	// A simple versioning to be safe. If you make a breaking change in the type, bump the version.
	// Any old records in the cache will just be ignored.
	version: typeof TEST_WEBHOOK_REGISTRATION_VERSION;
	pushRef?: string;
	workflowEntity: IWorkflowBase;
	destinationNode?: IDestinationNode;
	webhook: IWebhookData;
};

// Type guard for TestWebhookRegistration.
// NOTE: we could have a more robust validation, but this is probably good enough for now.
function isTestWebhookRegistration(obj: unknown): obj is TestWebhookRegistration {
	if (!isObjectLiteral(obj)) {
		return false;
	}

	if (!('version' in obj)) return false;

	return obj.version === TEST_WEBHOOK_REGISTRATION_VERSION;
}

@Service()
export class TestWebhookRegistrationsService {
	constructor(
		private readonly cacheService: CacheService,
		private readonly instanceSettings: InstanceSettings,
	) {}

	private readonly cacheKey = 'test-webhooks';

	async register(registration: TestWebhookRegistration) {
		const hashKey = this.toKey(registration.webhook);

		await this.cacheService.setHash(this.cacheKey, { [hashKey]: registration });

		const isCached = await this.cacheService.exists(this.cacheKey);

		if (!isCached) {
			throw new UserError(
				'Test webhook registration failed: workflow is too big. Remove pinned data',
			);
		}

		if (this.instanceSettings.isSingleMain) return;

		/**
		 * Multi-main setup: In a manual webhook execution, the main process that
		 * handles a webhook might not be the same as the main process that created
		 * the webhook. If so, after the test webhook has been successfully executed,
		 * the handler process commands the creator process to clear its test webhooks.
		 * We set a TTL on the key so that it is cleared even on creator process crash,
		 * with an additional buffer to ensure this safeguard expiration will not delete
		 * the key before the regular test webhook timeout fetches the key to delete it.
		 */
		const ttl = TEST_WEBHOOK_TIMEOUT + TEST_WEBHOOK_TIMEOUT_BUFFER;

		await this.cacheService.expire(this.cacheKey, ttl);
	}

	async deregister(arg: IWebhookData | string) {
		if (typeof arg === 'string') {
			await this.cacheService.deleteFromHash(this.cacheKey, arg);
		} else {
			const hashKey = this.toKey(arg);
			await this.cacheService.deleteFromHash(this.cacheKey, hashKey);
		}
	}

	async get(key: string): Promise<TestWebhookRegistration | undefined> {
		const val = await this.cacheService.getHashValue(this.cacheKey, key);
		return isTestWebhookRegistration(val) ? val : undefined;
	}

	async getAllKeys() {
		const hash = await this.cacheService.getHash<TestWebhookRegistration>(this.cacheKey);

		if (!hash) return [];

		return Object.keys(hash);
	}

	async getAllRegistrations() {
		const hash = await this.cacheService.getHash<TestWebhookRegistration>(this.cacheKey);

		if (!hash) return [];

		return Object.values(hash).filter(isTestWebhookRegistration);
	}

	async getRegistrationsHash() {
		const val = await this.cacheService.getHash<TestWebhookRegistration>(this.cacheKey);
		for (const key in val) {
			if (!isTestWebhookRegistration(val[key])) {
				delete val[key];
			}
		}
		return val;
	}

	toKey(webhook: Pick<IWebhookData, 'webhookId' | 'httpMethod' | 'path'>) {
		const { webhookId, httpMethod, path: webhookPath } = webhook;

		if (!webhookId) return [httpMethod, webhookPath].join('|');

		let path = webhookPath;

		if (path.startsWith(webhookId)) {
			const cutFromIndex = path.indexOf('/') + 1;

			path = path.slice(cutFromIndex);
		}

		return [httpMethod, webhookId, path.split('/').length].join('|');
	}
}
