"""
MIGRATION-META:
  source_path: packages/cli/src/modules/mcp/mcp.oauth-clients.controller.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/modules/mcp 的OAuth控制器。导入/依赖:外部:express；内部:@n8n/backend-common、@n8n/db、@n8n/decorators、@/errors/…/not-found.error；本地:./mcp-oauth-service。导出:McpOAuthClientsController。关键函数/方法:getAllClients、deleteClient。用于处理OAuth接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/mcp/mcp.oauth-clients.controller.ts -> services/n8n/presentation/cli/api/modules/mcp/mcp_oauth_clients_controller.py

import {
	DeleteOAuthClientResponseDto,
	ListOAuthClientsResponseDto,
	OAuthClientResponseDto,
} from '@n8n/api-types';
import { Logger } from '@n8n/backend-common';
import { AuthenticatedRequest } from '@n8n/db';
import { Delete, Get, GlobalScope, Param, RestController } from '@n8n/decorators';
import type { Response } from 'express';

import { NotFoundError } from '@/errors/response-errors/not-found.error';

import { McpOAuthService } from './mcp-oauth-service';

@RestController('/mcp/oauth-clients')
export class McpOAuthClientsController {
	constructor(
		private readonly mcpOAuthService: McpOAuthService,
		private readonly logger: Logger,
	) {}

	/**
	 * Get all OAuth clients for the current user
	 */
	@GlobalScope('mcp:oauth')
	@Get('/')
	async getAllClients(
		req: AuthenticatedRequest,
		_res: Response,
	): Promise<ListOAuthClientsResponseDto> {
		this.logger.debug('Fetching all OAuth clients for user', { userId: req.user.id });

		const clients = await this.mcpOAuthService.getAllClients(req.user.id);

		this.logger.debug(`Found ${clients.length} OAuth clients`);

		const clientDtos: OAuthClientResponseDto[] = clients.map((client) => ({
			id: client.id,
			name: client.name,
			redirectUris: client.redirectUris,
			grantTypes: client.grantTypes,
			tokenEndpointAuthMethod: client.tokenEndpointAuthMethod,
			createdAt: client.createdAt.toISOString(),
			updatedAt: client.updatedAt.toISOString(),
		}));

		return {
			data: clientDtos,
			count: clients.length,
		};
	}

	/**
	 * Delete an OAuth client by ID
	 * This will cascade delete all related tokens, authorization codes, and user consents
	 */
	@GlobalScope('mcp:oauth')
	@Delete('/:clientId')
	async deleteClient(
		req: AuthenticatedRequest,
		_res: Response,
		@Param('clientId') clientId: string,
	): Promise<DeleteOAuthClientResponseDto> {
		this.logger.info('Deleting OAuth client', {
			clientId,
			userId: req.user.id,
			userEmail: req.user.email,
		});

		try {
			await this.mcpOAuthService.deleteClient(clientId);

			this.logger.info('OAuth client deleted successfully', {
				clientId,
				userId: req.user.id,
			});

			return {
				success: true,
				message: `OAuth client ${clientId} has been deleted successfully`,
			};
		} catch (error) {
			if (error instanceof Error && error.message.includes('not found')) {
				this.logger.warn('Attempted to delete non-existent OAuth client', {
					clientId,
					userId: req.user.id,
				});
				throw new NotFoundError(`OAuth client with ID ${clientId} not found`);
			}
			throw error;
		}
	}
}
