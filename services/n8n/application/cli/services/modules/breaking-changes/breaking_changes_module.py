"""
MIGRATION-META:
  source_path: packages/cli/src/modules/breaking-changes/breaking-changes.module.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/breaking-changes 的模块。导入/依赖:外部:无；内部:@n8n/decorators；本地:./breaking-changes.controller。导出:BreakingChangesModule。关键函数/方法:init。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/breaking-changes/breaking-changes.module.ts -> services/n8n/application/cli/services/modules/breaking-changes/breaking_changes_module.py

import type { ModuleInterface } from '@n8n/decorators';
import { BackendModule } from '@n8n/decorators';

@BackendModule({ name: 'breaking-changes' })
export class BreakingChangesModule implements ModuleInterface {
	async init() {
		await import('./breaking-changes.controller');
	}
}
