"""
MIGRATION-META:
  source_path: packages/cli/src/modules/chat-hub/chat-hub.settings.controller.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/modules/chat-hub 的控制器。导入/依赖:外部:无；内部:@n8n/backend-common、@n8n/db、@n8n/decorators、@/errors/…/bad-request.error；本地:./chat-hub.settings.service。导出:ChatHubSettingsController。关键函数/方法:getSettings、getProviderSettings、updateSettings。用于处理该模块接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected @RestController/@Controller from @n8n/decorators
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/chat-hub/chat-hub.settings.controller.ts -> services/n8n/presentation/cli/api/v1/controllers/modules/chat-hub/chat_hub_settings_controller.py

import { ModuleRegistry, Logger } from '@n8n/backend-common';
import { type AuthenticatedRequest } from '@n8n/db';
import { Body, Get, Post, RestController, GlobalScope, Param } from '@n8n/decorators';

import { ChatHubSettingsService } from './chat-hub.settings.service';
import {
	ChatHubLLMProvider,
	chatHubLLMProviderSchema,
	UpdateChatSettingsRequest,
} from '@n8n/api-types';
import { BadRequestError } from '@/errors/response-errors/bad-request.error';

@RestController('/chat')
export class ChatHubSettingsController {
	constructor(
		private readonly settings: ChatHubSettingsService,
		private readonly logger: Logger,
		private readonly moduleRegistry: ModuleRegistry,
	) {}

	@Get('/settings')
	@GlobalScope('chatHub:manage')
	async getSettings(_req: AuthenticatedRequest, _res: Response) {
		const providers = await this.settings.getAllProviderSettings();
		return { providers };
	}

	@Get('/settings/:provider')
	@GlobalScope('chatHub:manage')
	async getProviderSettings(
		_req: AuthenticatedRequest,
		_res: Response,
		@Param('provider') provider: ChatHubLLMProvider,
	) {
		if (!chatHubLLMProviderSchema.safeParse(provider).success) {
			throw new BadRequestError(`Invalid provider: ${provider}`);
		}

		const settings = await this.settings.getProviderSettings(provider);
		return { settings };
	}

	@Post('/settings')
	@GlobalScope('chatHub:manage')
	async updateSettings(
		_req: AuthenticatedRequest,
		_res: Response,
		@Body body: UpdateChatSettingsRequest,
	) {
		const { payload } = body;
		await this.settings.setProviderSettings(payload.provider, payload);
		try {
			await this.moduleRegistry.refreshModuleSettings('chat-hub');
		} catch (error) {
			this.logger.warn('Failed to sync chat settings to module registry', {
				cause: error instanceof Error ? error.message : String(error),
			});
		}

		return await this.settings.getProviderSettings(payload.provider);
	}
}
