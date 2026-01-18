"""
MIGRATION-META:
  source_path: packages/@n8n/decorators/src/module/module-metadata.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/decorators/src/module 的模块。导入/依赖:外部:无；内部:@n8n/constants、@n8n/di；本地:./module。导出:ModuleMetadata。关键函数/方法:register、get、getEntries、getClasses。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/decorators/src/module/module-metadata.ts -> services/n8n/application/n8n-decorators/services/module/module_metadata.py

import type { InstanceType } from '@n8n/constants';
import { Service } from '@n8n/di';

import type { LicenseFlag, ModuleClass } from './module';

/**
 * Internal representation of a registered module.
 * For field descriptions, see {@link BackendModuleOptions}.
 */
type ModuleEntry = {
	class: ModuleClass;
	licenseFlag?: LicenseFlag | LicenseFlag[];
	instanceTypes?: InstanceType[];
};

@Service()
export class ModuleMetadata {
	private readonly modules: Map<string, ModuleEntry> = new Map();

	register(moduleName: string, moduleEntry: ModuleEntry) {
		this.modules.set(moduleName, moduleEntry);
	}

	get(moduleName: string) {
		return this.modules.get(moduleName);
	}

	getEntries() {
		return [...this.modules.entries()];
	}

	getClasses() {
		return [...this.modules.values()].map((entry) => entry.class);
	}
}
