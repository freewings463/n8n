"""
MIGRATION-META:
  source_path: packages/node-dev/src/Create.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/node-dev/src 的模块。导入/依赖:外部:fs/promises、replace-in-file；内部:无；本地:无。导出:无。关键函数/方法:createTemplate。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected runtime IO/external interaction -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/node-dev/src/Create.ts -> services/n8n/infrastructure/node-dev/container/Create.py

import { copyFile } from 'fs/promises';
import type { ReplaceInFileConfig } from 'replace-in-file';
import { replaceInFile } from 'replace-in-file';

/**
 * Creates a new credentials or node
 *
 * @param {string} sourceFilePath The path to the source template file
 * @param {string} destinationFilePath The path the write the new file to
 * @param {object} replaceValues The values to replace in the template file
 */
export async function createTemplate(
	sourceFilePath: string,
	destinationFilePath: string,
	replaceValues: object,
): Promise<void> {
	// Copy the file to then replace the values in it

	await copyFile(sourceFilePath, destinationFilePath);

	// Replace the variables in the template file
	const options: ReplaceInFileConfig = {
		files: [destinationFilePath],
		from: [],
		to: [],
	};
	options.from = Object.keys(replaceValues).map((key) => {
		return new RegExp(key, 'g');
	});
	options.to = Object.values(replaceValues);
	await replaceInFile(options);
}
