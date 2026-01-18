"""
MIGRATION-META:
  source_path: packages/cli/src/zod-alias-support.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src 的模块。导入/依赖:外部:zod；内部:无；本地:无。导出:无。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/zod-alias-support.ts -> services/n8n/application/cli/services/zod_alias_support.py

import { z } from 'zod';

// Monkey-patch zod to support aliases
declare module 'zod' {
	interface ZodType {
		alias<T extends ZodType>(this: T, aliasName: string): T;
	}
	interface ZodTypeDef {
		_alias: string;
	}
}

z.ZodType.prototype.alias = function <T extends z.ZodType>(this: T, aliasName: string) {
	this._def._alias = aliasName;
	return this;
};
