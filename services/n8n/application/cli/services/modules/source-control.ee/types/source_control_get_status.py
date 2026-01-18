"""
MIGRATION-META:
  source_path: packages/cli/src/modules/source-control.ee/types/source-control-get-status.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/source-control.ee/types 的类型。导入/依赖:外部:class-validator；内部:无；本地:无。导出:SourceControlGetStatus。关键函数/方法:booleanFromString。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/source-control.ee/types/source-control-get-status.ts -> services/n8n/application/cli/services/modules/source-control.ee/types/source_control_get_status.py

import { IsBoolean, IsOptional, IsString } from 'class-validator';

function booleanFromString(value: string | boolean): boolean {
	if (typeof value === 'boolean') {
		return value;
	}
	return value === 'true';
}

export class SourceControlGetStatus {
	@IsString()
	@IsOptional()
	direction: 'push' | 'pull';

	@IsBoolean()
	@IsOptional()
	preferLocalVersion: boolean;

	@IsBoolean()
	@IsOptional()
	verbose: boolean;

	constructor(values: {
		direction: 'push' | 'pull';
		preferLocalVersion: string | boolean;
		verbose: string | boolean;
	}) {
		this.direction = values.direction || 'push';
		this.preferLocalVersion = booleanFromString(values.preferLocalVersion) || true;
		this.verbose = booleanFromString(values.verbose) || false;
	}
}
