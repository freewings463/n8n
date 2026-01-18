"""
MIGRATION-META:
  source_path: packages/core/src/nodes-loader/package-directory-loader.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/core/src/nodes-loader 的模块。导入/依赖:外部:node:fs/promises；内部:n8n-workflow；本地:./directory-loader、./types。导出:PackageDirectoryLoader。关键函数/方法:inferSupportedNodes。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected runtime IO/external interaction -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/nodes-loader/package-directory-loader.ts -> services/n8n/infrastructure/core/container/nodes-loader/package_directory_loader.py

import { ApplicationError, jsonParse } from 'n8n-workflow';
import { readFileSync } from 'node:fs';
import { readFile } from 'node:fs/promises';

import { DirectoryLoader } from './directory-loader';
import type { n8n } from './types';

/**
 * Loader for source files of nodes and credentials located in a package dir,
 * e.g. /nodes-base or community packages.
 */
export class PackageDirectoryLoader extends DirectoryLoader {
	packageJson: n8n.PackageJson;

	packageName: string;

	constructor(directory: string, excludeNodes: string[] = [], includeNodes: string[] = []) {
		super(directory, excludeNodes, includeNodes);

		this.packageJson = this.readJSONSync('package.json');
		this.packageName = this.packageJson.name;

		this.excludeNodes = this.extractNodeTypes(excludeNodes, this.packageName);
		this.includeNodes = this.extractNodeTypes(includeNodes, this.packageName);
	}

	override async loadAll() {
		const { n8n, version, name } = this.packageJson;
		if (!n8n) return;

		const { nodes, credentials } = n8n;

		const packageVersion = !['n8n-nodes-base', '@n8n/n8n-nodes-langchain'].includes(name)
			? version
			: undefined;

		if (Array.isArray(nodes)) {
			for (const nodePath of nodes) {
				this.loadNodeFromFile(nodePath, packageVersion);
			}
		}

		if (Array.isArray(credentials)) {
			for (const credentialPath of credentials) {
				this.loadCredentialFromFile(credentialPath);
			}
		}

		this.inferSupportedNodes();

		this.logger.debug(`Loaded all credentials and nodes from ${this.packageName}`, {
			credentials: credentials?.length ?? 0,
			nodes: nodes?.length ?? 0,
		});
	}

	private inferSupportedNodes() {
		const knownCredentials = this.known.credentials;
		for (const { type: credentialType } of Object.values(this.credentialTypes)) {
			const supportedNodes = knownCredentials[credentialType.name].supportedNodes ?? [];
			if (supportedNodes.length > 0 && credentialType.httpRequestNode) {
				credentialType.httpRequestNode.hidden = true;
			}

			credentialType.supportedNodes = supportedNodes;

			if (!credentialType.iconUrl && !credentialType.icon) {
				for (const supportedNode of supportedNodes) {
					const nodeDescription = this.nodeTypes[supportedNode]?.type.description;

					if (!nodeDescription) continue;
					if (nodeDescription.icon) {
						credentialType.icon = nodeDescription.icon;
						credentialType.iconColor = nodeDescription.iconColor;
						break;
					}
					if (nodeDescription.iconUrl) {
						credentialType.iconUrl = nodeDescription.iconUrl;
						break;
					}
				}
			}
		}
	}

	private parseJSON<T>(fileString: string, filePath: string): T {
		try {
			return jsonParse<T>(fileString);
		} catch (error) {
			throw new ApplicationError('Failed to parse JSON', { extra: { filePath } });
		}
	}

	protected readJSONSync<T>(file: string): T {
		const filePath = this.resolvePath(file);
		const fileString = readFileSync(filePath, 'utf8');
		return this.parseJSON<T>(fileString, filePath);
	}

	protected async readJSON<T>(file: string): Promise<T> {
		const filePath = this.resolvePath(file);
		const fileString = await readFile(filePath, 'utf8');
		return this.parseJSON<T>(fileString, filePath);
	}
}
