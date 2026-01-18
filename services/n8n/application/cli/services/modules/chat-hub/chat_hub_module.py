"""
MIGRATION-META:
  source_path: packages/cli/src/modules/chat-hub/chat-hub.module.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/chat-hub 的模块。导入/依赖:外部:无；内部:@n8n/decorators、@n8n/di；本地:./chat-hub.controller、./chat-hub.settings.controller、./chat-hub.settings.service、./chat-hub-session.entity 等2项。导出:ChatHubModule。关键函数/方法:init、settings、entities、shutdown。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/chat-hub/chat-hub.module.ts -> services/n8n/application/cli/services/modules/chat-hub/chat_hub_module.py

import type { ModuleInterface } from '@n8n/decorators';
import { BackendModule, OnShutdown } from '@n8n/decorators';
import { Container } from '@n8n/di';

@BackendModule({ name: 'chat-hub' })
export class ChatHubModule implements ModuleInterface {
	async init() {
		await import('./chat-hub.controller');
		await import('./chat-hub.settings.controller');
	}

	async settings() {
		const { ChatHubSettingsService } = await import('./chat-hub.settings.service');
		const enabled = await Container.get(ChatHubSettingsService).getEnabled();
		const providers = await Container.get(ChatHubSettingsService).getAllProviderSettings();

		return { enabled, providers };
	}

	async entities() {
		const { ChatHubSession } = await import('./chat-hub-session.entity');
		const { ChatHubMessage } = await import('./chat-hub-message.entity');
		const { ChatHubAgent } = await import('./chat-hub-agent.entity');

		return [ChatHubSession, ChatHubMessage, ChatHubAgent];
	}

	@OnShutdown()
	async shutdown() {}
}
