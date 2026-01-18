"""
MIGRATION-META:
  source_path: packages/@n8n/config/src/custom-types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/config/src 的类型。导入/依赖:外部:无；内部:无；本地:无。导出:CommaSeparatedStringArray、ColonSeparatedStringArray。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/config treated as infrastructure configuration/runtime environment
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/config/src/custom-types.ts -> services/n8n/infrastructure/n8n-config/configuration/custom_types.py

abstract class StringArray<T extends string> extends Array<T> {
	constructor(str: string, delimiter: string) {
		super();
		const parsed = str.split(delimiter) as this;
		return parsed.filter((i) => typeof i === 'string' && i.length);
	}
}

export class CommaSeparatedStringArray<T extends string> extends StringArray<T> {
	constructor(str: string) {
		super(str, ',');
	}
}

export class ColonSeparatedStringArray<T extends string = string> extends StringArray<T> {
	constructor(str: string) {
		super(str, ':');
	}
}
