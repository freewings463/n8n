"""
MIGRATION-META:
  source_path: packages/cli/src/modules/community-packages/community-packages.module.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/community-packages 的模块。导入/依赖:外部:无；内部:@n8n/decorators、@n8n/di、n8n-core；本地:./community-packages.controller、./community-node-types.controller、./installed-nodes.entity、./installed-packages.entity 等1项。导出:CommunityPackagesModule。关键函数/方法:init、entities、settings、loadDir。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/community-packages/community-packages.module.ts -> services/n8n/application/cli/services/modules/community-packages/community_packages_module.py

import type { EntityClass, ModuleInterface } from '@n8n/decorators';
import { BackendModule } from '@n8n/decorators';
import { Container } from '@n8n/di';
import { InstanceSettings } from 'n8n-core';
import path from 'node:path';

@BackendModule({ name: 'community-packages' })
export class CommunityPackagesModule implements ModuleInterface {
	async init() {
		await import('./community-packages.controller');
		await import('./community-node-types.controller');
	}

	async entities() {
		const { InstalledNodes } = await import('./installed-nodes.entity');
		const { InstalledPackages } = await import('./installed-packages.entity');

		return [InstalledNodes, InstalledPackages] as EntityClass[];
	}

	async settings() {
		const { CommunityPackagesConfig } = await import('./community-packages.config');

		return {
			communityNodesEnabled: Container.get(CommunityPackagesConfig).enabled,
			unverifiedCommunityNodesEnabled: Container.get(CommunityPackagesConfig).unverifiedEnabled,
		};
	}

	async loadDir() {
		const { CommunityPackagesConfig } = await import('./community-packages.config');

		const { preventLoading } = Container.get(CommunityPackagesConfig);

		if (preventLoading) return null;

		return path.join(Container.get(InstanceSettings).nodesDownloadDir, 'node_modules');
	}
}
