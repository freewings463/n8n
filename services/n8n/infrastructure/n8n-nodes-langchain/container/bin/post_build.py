"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/scripts/post-build.js
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/scripts 的模块。导入/依赖:外部:无；内部:无；本地:无。导出:无。关键函数/方法:runCommand、execSync。用于承载该模块实现细节，并通过导出对外提供能力。注释目标:Post-build script / This is a separate script instead of inline npm commands because using "&&"" to chain commands in --onSuccess can cause the watch mode to hang。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected child_process execution -> infrastructure/container/bin
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/scripts/post-build.js -> services/n8n/infrastructure/n8n-nodes-langchain/container/bin/post_build.py

/**
 * Post-build script
 *
 * This is a separate script instead of inline npm commands because using "&&"" to chain commands in --onSuccess can cause the watch mode to hang
 */

const { execSync } = require('child_process');

function runCommand(command) {
	try {
		execSync(command, { stdio: 'inherit' });
	} catch (error) {
		console.error(`Command failed: ${command}`);
		process.exit(1);
	}
}

// Run all post-build tasks
runCommand('npx tsc-alias -p tsconfig.build.json');
runCommand('node scripts/copy-tokenizer-json.js .');
runCommand('node ../../nodes-base/scripts/copy-nodes-json.js .');
runCommand('pnpm n8n-copy-static-files');
runCommand('pnpm n8n-generate-metadata');
