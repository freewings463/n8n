"""
MIGRATION-META:
  source_path: packages/@n8n/backend-common/src/modules/errors/module-confusion.error.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/backend-common/src/modules/errors 的错误。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:ModuleConfusionError。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/backend-common treated as infrastructure configuration/runtime environment
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/backend-common/src/modules/errors/module-confusion.error.ts -> services/n8n/infrastructure/n8n-backend-common/configuration/modules/errors/module_confusion_error.py

import { UserError } from 'n8n-workflow';

export class ModuleConfusionError extends UserError {
	constructor(moduleNames: string[]) {
		const modules = moduleNames.length > 1 ? 'modules' : 'a module';

		super(
			`Found ${modules} listed in both \`N8N_ENABLED_MODULES\` and \`N8N_DISABLED_MODULES\`: ${moduleNames.join(', ')}. Please review your environment variables, as a module cannot be both enabled and disabled.`,
		);
	}
}
