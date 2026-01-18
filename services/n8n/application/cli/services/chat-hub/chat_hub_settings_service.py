"""
MIGRATION-META:
  source_path: packages/cli/src/modules/chat-hub/chat-hub.settings.service.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/chat-hub 的服务。导入/依赖:外部:无；内部:@/errors/…/bad-request.error、@n8n/db、@n8n/di、n8n-workflow；本地:无。导出:ChatHubSettingsService。关键函数/方法:CHAT_PROVIDER_SETTINGS_KEY、getDefaultProviderSettings、getEnabled、setEnabled、ensureModelIsAllowed、getProviderSettings、getAllProviderSettings、setProviderSettings。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/chat-hub/chat-hub.settings.service.ts -> services/n8n/application/cli/services/chat-hub/chat_hub_settings_service.py

import { BadRequestError } from '@/errors/response-errors/bad-request.error';
import {
	ChatHubConversationModel,
	ChatHubLLMProvider,
	chatHubLLMProviderSchema,
	ChatProviderSettingsDto,
} from '@n8n/api-types';
import { SettingsRepository } from '@n8n/db';
import { Service } from '@n8n/di';
import { jsonParse } from 'n8n-workflow';

const CHAT_PROVIDER_SETTINGS_KEY_PREFIX = 'chat.provider.';
const CHAT_PROVIDER_SETTINGS_KEY = (provider: ChatHubLLMProvider) =>
	`${CHAT_PROVIDER_SETTINGS_KEY_PREFIX}${provider}`;
const CHAT_ENABLED_KEY = 'chat.access.enabled';

const getDefaultProviderSettings = (provider: ChatHubLLMProvider): ChatProviderSettingsDto => ({
	provider,
	credentialId: null,
	allowedModels: [],
	createdAt: new Date().toISOString(),
	updatedAt: null,
	enabled: true,
});

@Service()
export class ChatHubSettingsService {
	constructor(private readonly settingsRepository: SettingsRepository) {}

	async getEnabled(): Promise<boolean> {
		const row = await this.settingsRepository.findByKey(CHAT_ENABLED_KEY);
		// Allowed by default
		if (!row) return true;
		return row.value === 'true';
	}

	async setEnabled(enabled: boolean): Promise<void> {
		const value = enabled ? 'true' : 'false';
		await this.settingsRepository.upsert({ key: CHAT_ENABLED_KEY, value, loadOnStartup: true }, [
			'key',
		]);
	}

	async ensureModelIsAllowed(model: ChatHubConversationModel): Promise<void> {
		if (model.provider === 'custom-agent' || model.provider === 'n8n') {
			// Custom agents and n8n models are always allowed, for now
			return;
		}

		const settings = await this.getProviderSettings(model.provider);
		if (!settings.enabled) {
			throw new BadRequestError('Provider is not enabled');
		}

		if (
			settings.allowedModels.length > 0 &&
			!settings.allowedModels.some((m) => m.model === model.model)
		) {
			throw new BadRequestError(`Model ${model.model} is not allowed`);
		}

		return;
	}

	async getProviderSettings(provider: ChatHubLLMProvider): Promise<ChatProviderSettingsDto> {
		const settings = await this.settingsRepository.findByKey(CHAT_PROVIDER_SETTINGS_KEY(provider));
		if (!settings) {
			return getDefaultProviderSettings(provider);
		}

		return jsonParse<ChatProviderSettingsDto>(settings.value, {
			fallbackValue: getDefaultProviderSettings(provider),
		});
	}

	async getAllProviderSettings(): Promise<Record<ChatHubLLMProvider, ChatProviderSettingsDto>> {
		const settings = await this.settingsRepository.findByKeyPrefix(
			CHAT_PROVIDER_SETTINGS_KEY_PREFIX,
		);

		const persistedByProvider = new Map<ChatHubLLMProvider, ChatProviderSettingsDto>();

		for (const setting of settings) {
			const parsed = jsonParse<ChatProviderSettingsDto>(setting.value);
			persistedByProvider.set(parsed.provider, parsed);
		}

		const result = {} as Record<ChatHubLLMProvider, ChatProviderSettingsDto>;

		// Ensure each provider has settings (use default if missing)
		for (const provider of chatHubLLMProviderSchema.options) {
			result[provider] = persistedByProvider.get(provider) ?? getDefaultProviderSettings(provider);
		}

		return result;
	}

	async setProviderSettings(
		provider: ChatHubLLMProvider,
		settings: ChatProviderSettingsDto,
	): Promise<void> {
		const value = JSON.stringify({
			...settings,
			createdAt: settings.createdAt ?? new Date().toISOString(),
			updatedAt: new Date().toISOString(),
		});

		await this.settingsRepository.upsert(
			{ key: CHAT_PROVIDER_SETTINGS_KEY(provider), value, loadOnStartup: true },
			['key'],
		);
	}
}
