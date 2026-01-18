"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/modules.d.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/node-cli/src 的类型。导入/依赖:外部:eslint；内部:无；本地:无。导出:无。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI package default -> presentation/cli
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/modules.d.ts -> services/n8n/presentation/n8n-node-cli/cli/modules_d.py

declare module 'eslint-plugin-n8n-nodes-base' {
	import type { ESLint } from 'eslint';

	const plugin: ESLint.Plugin & {
		configs: {
			community: {
				rules: Record<string, Linter.RuleEntry>;
			};
			credentials: {
				rules: Record<string, Linter.RuleEntry>;
			};
			nodes: {
				rules: Record<string, Linter.RuleEntry>;
			};
		};
	};

	export default plugin;
}
