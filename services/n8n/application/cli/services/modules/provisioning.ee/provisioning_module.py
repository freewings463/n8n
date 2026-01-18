"""
MIGRATION-META:
  source_path: packages/cli/src/modules/provisioning.ee/provisioning.module.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/provisioning.ee 的模块。导入/依赖:外部:无；内部:@n8n/decorators；本地:./provisioning.controller.ee。导出:ProvisioningModule。关键函数/方法:init。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/provisioning.ee/provisioning.module.ts -> services/n8n/application/cli/services/modules/provisioning.ee/provisioning_module.py

import type { ModuleInterface } from '@n8n/decorators';
import { BackendModule } from '@n8n/decorators';

@BackendModule({ name: 'provisioning', licenseFlag: ['feat:oidc', 'feat:saml', 'feat:ldap'] })
export class ProvisioningModule implements ModuleInterface {
	async init() {
		await import('./provisioning.controller.ee');
	}
}
