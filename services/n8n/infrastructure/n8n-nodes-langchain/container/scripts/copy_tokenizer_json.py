"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/scripts/copy-tokenizer-json.js
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/scripts 的模块。导入/依赖:外部:fast-glob；内部:无；本地:无。导出:无。关键函数/方法:copyTokenizerJsonFiles。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected runtime IO/external interaction -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/scripts/copy-tokenizer-json.js -> services/n8n/infrastructure/n8n-nodes-langchain/container/scripts/copy_tokenizer_json.py

const glob = require('fast-glob');
const fs = require('fs');
const path = require('path');

function copyTokenizerJsonFiles(baseDir) {
	// Make sure the target directory exists
	const targetDir = path.resolve(baseDir, 'dist', 'utils', 'tokenizer');
	if (!fs.existsSync(targetDir)) {
		fs.mkdirSync(targetDir, { recursive: true });
	}
	// Copy all tokenizer JSON files
	const files = glob.sync('utils/tokenizer/*.json', { cwd: baseDir });
	for (const file of files) {
		const sourcePath = path.resolve(baseDir, file);
		const targetPath = path.resolve(baseDir, 'dist', file);
		fs.copyFileSync(sourcePath, targetPath);
		console.log(`Copied: ${file} -> dist/${file}`);
	}
}

copyTokenizerJsonFiles(process.argv[2] || '.');
