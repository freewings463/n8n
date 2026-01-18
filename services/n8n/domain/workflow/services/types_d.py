"""
MIGRATION-META:
  source_path: packages/workflow/src/types.d.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src 的工作流类型。导入/依赖:外部:无；内部:无；本地:无。导出:无。关键函数/方法:set、toJSON。用于定义工作流相关类型/结构约束，供多模块共享。注释目标:/ <reference lib="es2022.error" />。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package workflow treated as domain model & rules
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/types.d.ts -> services/n8n/domain/workflow/services/types_d.py

/// <reference lib="es2022.error" />

declare module '@n8n_io/riot-tmpl' {
	interface Brackets {
		set(token: string): void;
	}

	type ReturnValue = string | null | (() => unknown);
	type TmplFn = (value: string, data: unknown) => ReturnValue;
	interface Tmpl extends TmplFn {
		errorHandler?(error: Error): void;
	}

	let brackets: Brackets;
	let tmpl: Tmpl;
}

interface BigInt {
	toJSON(): string;
}
