"""
MIGRATION-META:
  source_path: packages/cli/src/utils/handlebars.util.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/utils 的工具。导入/依赖:外部:express-handlebars；内部:无；本地:无。导出:createHandlebarsEngine。关键函数/方法:createHandlebarsEngine。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/utils/handlebars.util.ts -> services/n8n/application/cli/services/utils/handlebars_util.py

import { engine as expressHandlebars } from 'express-handlebars';

/**
 * Creates a configured Handlebars engine for express with custom helpers
 */
export function createHandlebarsEngine() {
	return expressHandlebars({
		defaultLayout: false,
		helpers: {
			eq: (a: unknown, b: unknown) => a === b,
			includes: (arr: unknown, val: unknown) => {
				if (Array.isArray(arr)) {
					return arr.includes(val);
				}
				if (typeof arr === 'string' && typeof val === 'string') {
					// Handle single string match or comma-separated strings
					if (arr === val) {
						return true;
					}
					return arr
						.split(',')
						.map((s) => s.trim())
						.includes(val);
				}
				return false;
			},
		},
	});
}
