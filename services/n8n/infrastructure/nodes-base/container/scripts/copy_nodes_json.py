"""
MIGRATION-META:
  source_path: packages/nodes-base/scripts/copy-nodes-json.js
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/scripts 的模块。导入/依赖:外部:fast-glob；内部:无；本地:无。导出:无。关键函数/方法:copyJsonFiles。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected runtime IO/external interaction -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/scripts/copy-nodes-json.js -> services/n8n/infrastructure/nodes-base/container/scripts/copy_nodes_json.py

const glob = require('fast-glob');
const fs = require('fs');
const path = require('path');

function copyJsonFiles(baseDir) {
	const files = glob.sync('nodes/**/*.node{,.ee}.json', { cwd: baseDir });
	for (const file of files) {
		fs.copyFileSync(path.resolve(baseDir, file), path.resolve(baseDir, 'dist', file));
	}
}

copyJsonFiles(process.argv[2]);
