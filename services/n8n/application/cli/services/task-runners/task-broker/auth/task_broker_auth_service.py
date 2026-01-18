"""
MIGRATION-META:
  source_path: packages/cli/src/task-runners/task-broker/auth/task-broker-auth.service.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/task-runners/task-broker/auth 的认证服务。导入/依赖:外部:无；内部:@n8n/config、@n8n/constants、@n8n/di、@/services/…/cache.service；本地:无。导出:TaskBrokerAuthService。关键函数/方法:isValidAuthToken、createGrantToken、tryConsumeGrantToken、generateGrantToken、cacheKeyForGrantToken。用于封装认证业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/task-runners/task-broker/auth/task-broker-auth.service.ts -> services/n8n/application/cli/services/task-runners/task-broker/auth/task_broker_auth_service.py

import { GlobalConfig } from '@n8n/config';
import { Time } from '@n8n/constants';
import { Service } from '@n8n/di';
import { randomBytes, timingSafeEqual } from 'crypto';

import { CacheService } from '@/services/cache/cache.service';

const GRANT_TOKEN_TTL = 15 * Time.seconds.toMilliseconds;

@Service()
export class TaskBrokerAuthService {
	private readonly authToken = Buffer.from(this.globalConfig.taskRunners.authToken);

	constructor(
		private readonly globalConfig: GlobalConfig,
		private readonly cacheService: CacheService,
		// For unit testing purposes
		private readonly grantTokenTtl = GRANT_TOKEN_TTL,
	) {}

	isValidAuthToken(token: string) {
		const tokenBuffer = Buffer.from(token);
		if (tokenBuffer.length !== this.authToken.length) return false;

		return timingSafeEqual(tokenBuffer, this.authToken);
	}

	/**
	 * @returns grant token that can be used to establish a task runner connection
	 */
	async createGrantToken() {
		const grantToken = this.generateGrantToken();

		const key = this.cacheKeyForGrantToken(grantToken);
		await this.cacheService.set(key, '1', this.grantTokenTtl);

		return grantToken;
	}

	/**
	 * Checks if the given `grantToken` is a valid token and marks it as
	 * used.
	 */
	async tryConsumeGrantToken(grantToken: string) {
		const key = this.cacheKeyForGrantToken(grantToken);
		const consumed = await this.cacheService.get<string>(key);
		// Not found from cache --> Invalid token
		if (consumed === undefined) return false;

		await this.cacheService.delete(key);
		return true;
	}

	private generateGrantToken() {
		return randomBytes(32).toString('hex');
	}

	private cacheKeyForGrantToken(grantToken: string) {
		return `grant-token:${grantToken}`;
	}
}
