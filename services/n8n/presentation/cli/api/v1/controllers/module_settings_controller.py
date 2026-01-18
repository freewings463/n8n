"""
MIGRATION-META:
  source_path: packages/cli/src/controllers/module-settings.controller.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/controllers 的控制器。导入/依赖:外部:无；内部:@n8n/decorators、@/services/frontend.service；本地:无。导出:ModuleSettingsController。关键函数/方法:getModuleSettings。用于处理该模块接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected @RestController/@Controller from @n8n/decorators
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/controllers/module-settings.controller.ts -> services/n8n/presentation/cli/api/v1/controllers/module_settings_controller.py

import { Get, RestController } from '@n8n/decorators';

import { FrontendService } from '@/services/frontend.service';

@RestController('/module-settings')
export class ModuleSettingsController {
	constructor(private readonly frontendService: FrontendService) {}

	/**
	 * @returns settings for all loaded modules
	 */
	@Get('/')
	getModuleSettings() {
		return this.frontendService.getModuleSettings();
	}
}
