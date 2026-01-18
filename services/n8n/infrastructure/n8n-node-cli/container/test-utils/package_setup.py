"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/test-utils/package-setup.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/test-utils 的模块。导入/依赖:外部:node:fs/promises；内部:无；本地:../utils/package。导出:PackageSetupOptions。关键函数/方法:setupTestPackage。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected runtime IO/external interaction -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/test-utils/package-setup.ts -> services/n8n/infrastructure/n8n-node-cli/container/test-utils/package_setup.py

import fs from 'node:fs/promises';

import type { N8nPackageJson } from '../utils/package';

export interface PackageSetupOptions {
	packageJson?: Partial<N8nPackageJson>;
	eslintConfig?: string | boolean;
}

const DEFAULT_PACKAGE_CONFIG: N8nPackageJson = {
	name: 'test-node',
	version: '1.0.0',
	n8n: {
		nodes: ['dist/nodes/TestNode.node.js'],
		strict: true,
	},
};

const DEFAULT_ESLINT_CONFIG =
	"import { config } from '@n8n/node-cli/eslint';\n\nexport default config;\n";

export async function setupTestPackage(
	tmpdir: string,
	options: PackageSetupOptions = {},
): Promise<void> {
	const packageConfig = {
		...DEFAULT_PACKAGE_CONFIG,
		...options.packageJson,
		n8n: {
			...DEFAULT_PACKAGE_CONFIG.n8n,
			...options.packageJson?.n8n,
		},
	};
	await fs.writeFile(`${tmpdir}/package.json`, JSON.stringify(packageConfig, null, 2));

	if (options.eslintConfig === true) {
		await fs.writeFile(`${tmpdir}/eslint.config.mjs`, DEFAULT_ESLINT_CONFIG);
	} else if (typeof options.eslintConfig === 'string') {
		await fs.writeFile(`${tmpdir}/eslint.config.mjs`, options.eslintConfig);
	}
}
