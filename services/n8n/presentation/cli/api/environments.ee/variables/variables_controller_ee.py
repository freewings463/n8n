"""
MIGRATION-META:
  source_path: packages/cli/src/environments.ee/variables/variables.controller.ee.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/environments.ee/variables 的控制器。导入/依赖:外部:express；内部:@n8n/api-types、@n8n/db、@n8n/decorators、@/errors/…/bad-request.error、@/errors/…/not-found.error、@/errors/variable-count-limit-reached.error 等1项；本地:./variables.service.ee。导出:VariablesController。关键函数/方法:getVariables、createVariable、getVariable、updateVariable、deleteVariable。用于处理该模块接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/environments.ee/variables/variables.controller.ee.ts -> services/n8n/presentation/cli/api/environments.ee/variables/variables_controller_ee.py

import { CreateVariableRequestDto, VariableListRequestDto } from '@n8n/api-types';
import { AuthenticatedRequest } from '@n8n/db';
import { Body, Delete, Get, Licensed, Patch, Post, Query, RestController } from '@n8n/decorators';
import type { Response } from 'express';

import { BadRequestError } from '@/errors/response-errors/bad-request.error';
import { NotFoundError } from '@/errors/response-errors/not-found.error';
import { VariableCountLimitReachedError } from '@/errors/variable-count-limit-reached.error';
import { VariableValidationError } from '@/errors/variable-validation.error';

import { VariablesService } from './variables.service.ee';

@RestController('/variables')
export class VariablesController {
	constructor(private readonly variablesService: VariablesService) {}

	@Get('/')
	async getVariables(
		req: AuthenticatedRequest,
		_res: unknown,
		@Query query: VariableListRequestDto,
	) {
		return await this.variablesService.getAllForUser(req.user, query);
	}

	@Post('/')
	@Licensed('feat:variables')
	async createVariable(
		req: AuthenticatedRequest,
		_res: Response,
		@Body payload: CreateVariableRequestDto,
	) {
		try {
			return await this.variablesService.create(req.user, payload);
		} catch (error) {
			if (error instanceof VariableCountLimitReachedError) {
				throw new BadRequestError(error.message);
			} else if (error instanceof VariableValidationError) {
				throw new BadRequestError(error.message);
			}
			throw error;
		}
	}

	@Get('/:id')
	async getVariable(req: AuthenticatedRequest<{ id: string }>) {
		const variable = await this.variablesService.getForUser(req.user, req.params.id);
		if (variable === null) {
			throw new NotFoundError(`Variable with id ${req.params.id} not found`);
		}
		return variable;
	}

	@Patch('/:id')
	@Licensed('feat:variables')
	async updateVariable(
		req: AuthenticatedRequest<{ id: string }>,
		_res: Response,
		@Body payload: CreateVariableRequestDto,
	) {
		const id = req.params.id;
		try {
			return await this.variablesService.update(req.user, id, payload);
		} catch (error) {
			if (error instanceof VariableCountLimitReachedError) {
				throw new BadRequestError(error.message);
			} else if (error instanceof VariableValidationError) {
				throw new BadRequestError(error.message);
			}
			throw error;
		}
	}

	@Delete('/:id')
	@Licensed('feat:variables')
	async deleteVariable(req: AuthenticatedRequest<{ id: string }>) {
		await this.variablesService.deleteForUser(req.user, req.params.id);

		return true;
	}
}
