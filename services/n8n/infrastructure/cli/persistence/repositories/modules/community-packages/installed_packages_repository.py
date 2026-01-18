"""
MIGRATION-META:
  source_path: packages/cli/src/modules/community-packages/installed-packages.repository.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/modules/community-packages 的仓储。导入/依赖:外部:无；内部:@n8n/di、@n8n/typeorm、n8n-core；本地:./installed-nodes.repository、./installed-packages.entity。导出:InstalledPackagesRepository。关键函数/方法:saveInstalledPackageWithNodes。用于封装该模块数据读写与查询细节，隔离持久层。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected TypeORM Repository/EntityManager usage
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/community-packages/installed-packages.repository.ts -> services/n8n/infrastructure/cli/persistence/repositories/modules/community-packages/installed_packages_repository.py

import { Service } from '@n8n/di';
import { DataSource, Repository } from '@n8n/typeorm';
import type { PackageDirectoryLoader } from 'n8n-core';

import { InstalledNodesRepository } from './installed-nodes.repository';
import { InstalledPackages } from './installed-packages.entity';

@Service()
export class InstalledPackagesRepository extends Repository<InstalledPackages> {
	constructor(
		dataSource: DataSource,
		private installedNodesRepository: InstalledNodesRepository,
	) {
		super(InstalledPackages, dataSource.manager);
	}

	async saveInstalledPackageWithNodes(packageLoader: PackageDirectoryLoader) {
		const { packageJson, nodeTypes, loadedNodes } = packageLoader;
		const { name: packageName, version: installedVersion, author } = packageJson;

		let installedPackage: InstalledPackages;

		await this.manager.transaction(async (manager) => {
			installedPackage = await manager.save(
				this.create({
					packageName,
					installedVersion,
					authorName: author?.name,
					authorEmail: author?.email,
				}),
			);

			installedPackage.installedNodes = [];

			for (const loadedNode of loadedNodes) {
				const installedNode = this.installedNodesRepository.create({
					name: nodeTypes[loadedNode.name].type.description.displayName,
					type: `${packageName}.${loadedNode.name}`,
					latestVersion: loadedNode.version,
					package: { packageName },
				});

				installedPackage.installedNodes.push(installedNode);

				await manager.save(installedNode);
			}
		});

		return installedPackage!;
	}
}
