"""
MIGRATION-META:
  source_path: packages/core/src/nodes-loader/custom-directory-loader.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/core/src/nodes-loader 的模块。导入/依赖:外部:fast-glob；内部:无；本地:./constants、./directory-loader。导出:CustomDirectoryLoader。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node loading/discovery -> infrastructure/container/nodes_loader
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/nodes-loader/custom-directory-loader.ts -> services/n8n/infrastructure/core/container/nodes_loader/custom_directory_loader.py

import glob from 'fast-glob';

import { CUSTOM_NODES_PACKAGE_NAME } from './constants';
import { DirectoryLoader } from './directory-loader';

/**
 * Loader for source files of nodes and credentials located in a custom dir,
 * e.g. `~/.n8n/custom`
 */
export class CustomDirectoryLoader extends DirectoryLoader {
	packageName = CUSTOM_NODES_PACKAGE_NAME;

	constructor(directory: string, excludeNodes: string[] = [], includeNodes: string[] = []) {
		super(directory, excludeNodes, includeNodes);

		this.excludeNodes = this.extractNodeTypes(excludeNodes, this.packageName);
		this.includeNodes = this.extractNodeTypes(includeNodes, this.packageName);
	}

	override async loadAll() {
		const nodes = await glob('**/*.node.js', {
			cwd: this.directory,
			absolute: true,
		});

		for (const nodePath of nodes) {
			this.loadNodeFromFile(nodePath);
		}

		const credentials = await glob('**/*.credentials.js', {
			cwd: this.directory,
			absolute: true,
		});

		for (const credentialPath of credentials) {
			this.loadCredentialFromFile(credentialPath);
		}
	}
}
