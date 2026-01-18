"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/scripts/copy-templates.mjs
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/scripts 的模块。导入/依赖:外部:fast-glob、node:fs/promises；内部:无；本地:无。导出:无。关键函数/方法:cp。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected runtime IO/external interaction -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/scripts/copy-templates.mjs -> services/n8n/infrastructure/n8n-node-cli/container/scripts/copy_templates.py

#!/usr/bin/env node

import glob from 'fast-glob';
import { cp } from 'node:fs/promises';
import path from 'path';

const templateFiles = glob.sync(['src/template/templates/**/*'], {
	cwd: path.resolve(import.meta.dirname, '..'),
	ignore: ['**/node_modules', '**/dist'],
	dot: true,
});

await Promise.all(
	templateFiles.map((template) =>
		cp(template, `dist/${template.replace('src/', '')}`, { recursive: true }),
	),
);
