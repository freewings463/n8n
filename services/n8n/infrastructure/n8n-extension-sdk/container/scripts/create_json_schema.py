"""
MIGRATION-META:
  source_path: packages/@n8n/extension-sdk/scripts/create-json-schema.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/extension-sdk/scripts 的模块。导入/依赖:外部:zod-to-json-schema、fs/promises、prettier；内部:无；本地:../src/schema。导出:无。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected runtime IO/external interaction -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/extension-sdk/scripts/create-json-schema.ts -> services/n8n/infrastructure/n8n-extension-sdk/container/scripts/create_json_schema.py

import { extensionManifestSchema } from '../src/schema';
import { zodToJsonSchema } from 'zod-to-json-schema';
import { writeFile } from 'fs/promises';
import { dirname, resolve } from 'path';
import { fileURLToPath } from 'url';
import { format, resolveConfig } from 'prettier';

const __dirname = dirname(fileURLToPath(import.meta.url));
const rootDir = resolve(__dirname, '..');

const jsonSchema = zodToJsonSchema(extensionManifestSchema, {
	name: 'N8nExtensionSchema',
	nameStrategy: 'title',
});

(async () => {
	const filepath = 'schema.json';
	const schema = JSON.stringify(jsonSchema);
	const config = await resolveConfig(filepath);
	const formattedSchema = await format(schema, { ...config, filepath });
	await writeFile(resolve(rootDir, filepath), formattedSchema);
})();
