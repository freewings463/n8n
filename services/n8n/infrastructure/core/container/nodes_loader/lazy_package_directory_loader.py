"""
MIGRATION-META:
  source_path: packages/core/src/nodes-loader/lazy-package-directory-loader.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/core/src/nodes-loader 的模块。导入/依赖:外部:无；内部:无；本地:./package-directory-loader。导出:LazyPackageDirectoryLoader。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node loading/discovery -> infrastructure/container/nodes_loader
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/nodes-loader/lazy-package-directory-loader.ts -> services/n8n/infrastructure/core/container/nodes_loader/lazy_package_directory_loader.py

import { PackageDirectoryLoader } from './package-directory-loader';

/**
 * This loader extends PackageDirectoryLoader to load node and credentials lazily, if possible
 */
export class LazyPackageDirectoryLoader extends PackageDirectoryLoader {
	override async loadAll() {
		try {
			this.known.nodes = await this.readJSON('dist/known/nodes.json');
			this.known.credentials = await this.readJSON('dist/known/credentials.json');

			this.types.nodes = await this.readJSON('dist/types/nodes.json');
			this.types.credentials = await this.readJSON('dist/types/credentials.json');

			if (this.removeNonIncludedNodes) {
				const allowedNodes: typeof this.known.nodes = {};
				for (const nodeType of this.includeNodes) {
					if (nodeType in this.known.nodes) {
						allowedNodes[nodeType] = this.known.nodes[nodeType];
					}
				}
				this.known.nodes = allowedNodes;

				this.types.nodes = this.types.nodes.filter((nodeType) =>
					this.includeNodes.includes(nodeType.name),
				);
			}

			if (this.excludeNodes.length) {
				for (const nodeType of this.excludeNodes) {
					delete this.known.nodes[nodeType];
				}

				this.types.nodes = this.types.nodes.filter(
					(nodeType) => !this.excludeNodes.includes(nodeType.name),
				);
			}

			this.logger.debug(`Lazy-loading nodes and credentials from ${this.packageJson.name}`, {
				nodes: this.types.nodes?.length ?? 0,
				credentials: this.types.credentials?.length ?? 0,
			});

			this.isLazyLoaded = true;

			return; // We can load nodes and credentials lazily now
		} catch {
			this.logger.debug("Can't enable lazy-loading");
			await super.loadAll();
		}
	}
}
