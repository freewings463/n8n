"""
MIGRATION-META:
  source_path: packages/core/bin/common.js
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/core/bin 的模块。导入/依赖:外部:fs/promises；内部:无；本地:无。导出:无。关键函数/方法:writeJSON。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected runtime IO/external interaction -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/bin/common.js -> services/n8n/infrastructure/core/container/bin/common.py

const path = require('path');
const { mkdir, writeFile } = require('fs/promises');

const packageDir = process.cwd();
const distDir = path.join(packageDir, 'dist');

const writeJSON = async (file, data) => {
	const filePath = path.resolve(distDir, file);
	await mkdir(path.dirname(filePath), { recursive: true });
	const payload = Array.isArray(data)
		? `[\n${data.map((entry) => JSON.stringify(entry)).join(',\n')}\n]`
		: JSON.stringify(data, null, 2);
	await writeFile(filePath, payload, { encoding: 'utf-8' });
};

module.exports = {
	packageDir,
	writeJSON,
};
