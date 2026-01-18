"""
MIGRATION-META:
  source_path: packages/cli/src/task-runners/task-broker/auth/task-broker-auth.controller.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/task-runners/task-broker/auth 的认证控制器。导入/依赖:外部:express；内部:@n8n/di、@/requests、@/task-runners/…/task-broker-types；本地:./task-broker-auth.schema、./task-broker-auth.service、../response-errors/bad-request.error、../response-errors/forbidden.error。导出:TaskBrokerAuthController。关键函数/方法:createGrantToken、authMiddleware、next。用于处理认证接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected Express RequestHandler-style middleware
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/task-runners/task-broker/auth/task-broker-auth.controller.ts -> services/n8n/presentation/cli/api/middleware/task-runners/task-broker/auth/task_broker_auth_controller.py

import { Service } from '@n8n/di';
import type { NextFunction, Response } from 'express';

import type { AuthlessRequest } from '@/requests';
import type { TaskBrokerServerInitRequest } from '@/task-runners/task-broker/task-broker-types';

import { taskBrokerAuthRequestBodySchema } from './task-broker-auth.schema';
import { TaskBrokerAuthService } from './task-broker-auth.service';
import { BadRequestError } from '../../../errors/response-errors/bad-request.error';
import { ForbiddenError } from '../../../errors/response-errors/forbidden.error';

/**
 * Controller responsible for authenticating Task Runner connections
 */
@Service()
export class TaskBrokerAuthController {
	constructor(private readonly authService: TaskBrokerAuthService) {
		// eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
		this.authMiddleware = this.authMiddleware.bind(this);
	}

	/**
	 * Validates the provided auth token and creates and responds with a grant token,
	 * which can be used to initiate a task runner connection.
	 */
	async createGrantToken(req: AuthlessRequest) {
		const result = await taskBrokerAuthRequestBodySchema.safeParseAsync(req.body);
		if (!result.success) {
			throw new BadRequestError(result.error.errors[0].code);
		}

		const { token: authToken } = result.data;
		if (!this.authService.isValidAuthToken(authToken)) {
			throw new ForbiddenError();
		}

		const grantToken = await this.authService.createGrantToken();
		return {
			token: grantToken,
		};
	}

	/**
	 * Middleware to authenticate task runner init requests
	 */
	async authMiddleware(req: TaskBrokerServerInitRequest, res: Response, next: NextFunction) {
		const authHeader = req.headers.authorization;
		if (typeof authHeader !== 'string' || !authHeader.startsWith('Bearer ')) {
			res.status(401).json({ code: 401, message: 'Unauthorized' });
			return;
		}

		const grantToken = authHeader.slice('Bearer '.length);
		const isConsumed = await this.authService.tryConsumeGrantToken(grantToken);
		if (!isConsumed) {
			res.status(403).json({ code: 403, message: 'Forbidden' });
			return;
		}

		next();
	}
}
