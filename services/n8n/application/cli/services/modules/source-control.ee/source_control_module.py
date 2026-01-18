"""
MIGRATION-META:
  source_path: packages/cli/src/modules/source-control.ee/source-control.module.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/source-control.ee 的模块。导入/依赖:外部:无；内部:@n8n/decorators、@n8n/di；本地:./source-control.controller.ee、./source-control.service.ee。导出:SourceControlModule。关键函数/方法:init。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/source-control.ee/source-control.module.ts -> services/n8n/application/cli/services/modules/source-control.ee/source_control_module.py

import type { ModuleInterface } from '@n8n/decorators';
import { BackendModule } from '@n8n/decorators';
import { Container } from '@n8n/di';

@BackendModule({ name: 'source-control', licenseFlag: 'feat:sourceControl' })
export class SourceControlModule implements ModuleInterface {
	async init() {
		await import('./source-control.controller.ee');

		const { SourceControlService } = await import('./source-control.service.ee');
		await Container.get(SourceControlService).start();
	}
}
