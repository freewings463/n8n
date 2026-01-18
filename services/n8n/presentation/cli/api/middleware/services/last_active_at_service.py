"""
MIGRATION-META:
  source_path: packages/cli/src/services/last-active-at.service.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/services 的服务。导入/依赖:外部:express、luxon；内部:@n8n/backend-common、@n8n/db、@n8n/di；本地:无。导出:LastActiveAtService。关键函数/方法:middleware、next、updateLastActiveIfStale。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected Express RequestHandler-style middleware
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/services/last-active-at.service.ts -> services/n8n/presentation/cli/api/middleware/services/last_active_at_service.py

import { Logger } from '@n8n/backend-common';
import type { AuthenticatedRequest } from '@n8n/db';
import { UserRepository } from '@n8n/db';
import { Service } from '@n8n/di';
import type { NextFunction, Response } from 'express';
import { DateTime } from 'luxon';

@Service()
export class LastActiveAtService {
	private readonly lastActiveCache = new Map<string, string>();

	constructor(
		private readonly userRepository: UserRepository,
		private readonly logger: Logger,
	) {}

	async middleware(req: AuthenticatedRequest, _res: Response, next: NextFunction) {
		if (req.user) {
			this.updateLastActiveIfStale(req.user.id).catch((error: unknown) => {
				this.logger.error('Failed to update last active timestamp', { error });
			});
		}
		next();
	}

	async updateLastActiveIfStale(userId: string) {
		const now = DateTime.now().startOf('day');
		const dateNow = now.toISODate();
		const last = this.lastActiveCache.get(userId);

		// Update if date changed (or not set)
		if (!last || last !== dateNow) {
			await this.userRepository
				.createQueryBuilder()
				.update()
				.set({ lastActiveAt: now.toJSDate() })
				.where('id = :id', { id: userId })
				.execute();

			this.lastActiveCache.set(userId, dateNow);
		}
	}
}
