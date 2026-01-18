"""
MIGRATION-META:
  source_path: packages/cli/src/services/banner.service.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/services 的服务。导入/依赖:外部:无；内部:@n8n/api-types、@n8n/db、@n8n/di、n8n-core、@/config；本地:无。导出:BannerService。关键函数/方法:dismissBanner。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/services/banner.service.ts -> services/n8n/application/cli/services/banner_service.py

import type { BannerName } from '@n8n/api-types';
import { SettingsRepository } from '@n8n/db';
import { Service } from '@n8n/di';
import { ErrorReporter } from 'n8n-core';

import config from '@/config';

@Service()
export class BannerService {
	constructor(
		private readonly settingsRepository: SettingsRepository,
		private readonly errorReporter: ErrorReporter,
	) {}

	async dismissBanner(bannerName: BannerName) {
		const key = 'ui.banners.dismissed';
		const dismissedBannersSetting = await this.settingsRepository.findOneBy({ key });
		try {
			let value: string;
			if (dismissedBannersSetting) {
				const dismissedBanners = JSON.parse(dismissedBannersSetting.value) as string[];
				const updatedValue = [...new Set([...dismissedBanners, bannerName].sort())];
				value = JSON.stringify(updatedValue);
				await this.settingsRepository.update({ key }, { value, loadOnStartup: true });
			} else {
				value = JSON.stringify([bannerName]);
				await this.settingsRepository.save(
					{ key, value, loadOnStartup: true },
					{ transaction: false },
				);
			}
			config.set(key, value);
		} catch (error) {
			this.errorReporter.error(error);
		}
	}
}
