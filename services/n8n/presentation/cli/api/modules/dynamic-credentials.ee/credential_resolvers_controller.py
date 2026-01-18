"""
MIGRATION-META:
  source_path: packages/cli/src/modules/dynamic-credentials.ee/credential-resolvers.controller.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/modules/dynamic-credentials.ee 的控制器。导入/依赖:外部:express；内部:@n8n/db、@/errors/…/bad-request.error、@/errors/…/internal-server.error 等1项；本地:./errors/credential-resolver-not-found.error、./services/credential-resolver.service。导出:CredentialResolversController。关键函数/方法:listResolvers、listResolverTypes、createResolver、getResolver、updateResolver、deleteResolver。用于处理该模块接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/dynamic-credentials.ee/credential-resolvers.controller.ts -> services/n8n/presentation/cli/api/modules/dynamic-credentials.ee/credential_resolvers_controller.py

import {
	CreateCredentialResolverDto,
	CredentialResolver,
	credentialResolverSchema,
	credentialResolversSchema,
	UpdateCredentialResolverDto,
	CredentialResolverType,
	credentialResolverTypesSchema,
} from '@n8n/api-types';
import { AuthenticatedRequest } from '@n8n/db';
import {
	Body,
	Delete,
	Get,
	GlobalScope,
	Param,
	Patch,
	Post,
	RestController,
	CredentialResolverValidationError,
} from '@n8n/decorators';
import { Response } from 'express';

import { DynamicCredentialResolverNotFoundError } from './errors/credential-resolver-not-found.error';
import { DynamicCredentialResolverService } from './services/credential-resolver.service';

import { BadRequestError } from '@/errors/response-errors/bad-request.error';
import { InternalServerError } from '@/errors/response-errors/internal-server.error';
import { NotFoundError } from '@/errors/response-errors/not-found.error';

@RestController('/credential-resolvers')
export class CredentialResolversController {
	constructor(private readonly service: DynamicCredentialResolverService) {}

	@Get('/')
	@GlobalScope('credentialResolver:list')
	async listResolvers(_req: AuthenticatedRequest, _res: Response): Promise<CredentialResolver[]> {
		try {
			return credentialResolversSchema.parse(await this.service.findAll());
		} catch (e: unknown) {
			if (e instanceof Error) {
				throw new InternalServerError(e.message, e);
			}
			throw e;
		}
	}

	@Get('/types')
	@GlobalScope('credentialResolver:list')
	listResolverTypes(_req: AuthenticatedRequest, _res: Response): CredentialResolverType[] {
		try {
			const types = this.service.getAvailableTypes();
			return credentialResolverTypesSchema.parse(types.map((t) => t.metadata));
		} catch (e: unknown) {
			if (e instanceof Error) {
				throw new InternalServerError(e.message, e);
			}
			throw e;
		}
	}

	@Post('/')
	@GlobalScope('credentialResolver:create')
	async createResolver(
		req: AuthenticatedRequest,
		_res: Response,
		@Body dto: CreateCredentialResolverDto,
	): Promise<CredentialResolver> {
		try {
			const createdResolver = await this.service.create({
				name: dto.name,
				type: dto.type,
				config: dto.config,
				user: req.user,
			});
			return credentialResolverSchema.parse(createdResolver);
		} catch (e: unknown) {
			if (e instanceof CredentialResolverValidationError) {
				throw new BadRequestError(e.message);
			}
			if (e instanceof Error) {
				throw new InternalServerError(e.message, e);
			}
			throw e;
		}
	}

	@Get('/:id')
	@GlobalScope('credentialResolver:read')
	async getResolver(
		_req: AuthenticatedRequest,
		_res: Response,
		@Param('id') id: string,
	): Promise<CredentialResolver> {
		try {
			return credentialResolverSchema.parse(await this.service.findById(id));
		} catch (e: unknown) {
			if (e instanceof DynamicCredentialResolverNotFoundError) {
				throw new NotFoundError(e.message);
			}
			if (e instanceof Error) {
				throw new InternalServerError(e.message, e);
			}
			throw e;
		}
	}

	@Patch('/:id')
	@GlobalScope('credentialResolver:update')
	async updateResolver(
		req: AuthenticatedRequest,
		_res: Response,
		@Param('id') id: string,
		@Body dto: UpdateCredentialResolverDto,
	): Promise<CredentialResolver> {
		try {
			return credentialResolverSchema.parse(
				await this.service.update(id, {
					type: dto.type,
					name: dto.name,
					config: dto.config,
					clearCredentials: dto.clearCredentials,
					user: req.user,
				}),
			);
		} catch (e: unknown) {
			if (e instanceof DynamicCredentialResolverNotFoundError) {
				throw new NotFoundError(e.message);
			}
			if (e instanceof CredentialResolverValidationError) {
				throw new BadRequestError(e.message);
			}
			if (e instanceof Error) {
				throw new InternalServerError(e.message, e);
			}
			throw e;
		}
	}

	@Delete('/:id')
	@GlobalScope('credentialResolver:delete')
	async deleteResolver(
		_req: AuthenticatedRequest,
		_res: Response,
		@Param('id') id: string,
	): Promise<{ success: true }> {
		try {
			await this.service.delete(id);
			return { success: true };
		} catch (e: unknown) {
			if (e instanceof DynamicCredentialResolverNotFoundError) {
				throw new NotFoundError(e.message);
			}
			if (e instanceof Error) {
				throw new InternalServerError(e.message, e);
			}
			throw e;
		}
	}
}
