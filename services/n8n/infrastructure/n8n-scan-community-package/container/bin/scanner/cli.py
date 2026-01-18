"""
MIGRATION-META:
  source_path: packages/@n8n/scan-community-package/scanner/cli.mjs
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/scan-community-package/scanner 的模块。导入/依赖:外部:无；内部:无；本地:./scanner.mjs。导出:无。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Community package scanner CLI/tooling -> infrastructure/container/bin
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/scan-community-package/scanner/cli.mjs -> services/n8n/infrastructure/n8n-scan-community-package/container/bin/scanner/cli.py

#!/usr/bin/env node

const args = process.argv.slice(2);
if (args.length < 1) {
	console.error('Usage: npx @n8n/scan-community-package <package-name>[@version]');
	process.exit(1);
}

import { resolvePackage, analyzePackageByName } from './scanner.mjs';

const packageSpec = args[0];
const { packageName, version } = resolvePackage(packageSpec);
try {
	const result = await analyzePackageByName(packageName, version);

	if (result.passed) {
		console.log(`✅ Package ${packageName}@${result.version} has passed all security checks`);
	} else {
		console.log(`❌ Package ${packageName}@${result.version} has failed security checks`);
		console.log(`Reason: ${result.message}`);

		if (result.details) {
			console.log('\nDetails:');
			console.log(result.details);
		}
	}
} catch (error) {
	console.error('Analysis failed:', error);
	process.exit(1);
}
