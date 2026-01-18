"""
MIGRATION-META:
  source_path: packages/cli/src/modules/source-control.ee/types/source-control-context.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/source-control.ee/types 的类型。导入/依赖:外部:无；内部:@n8n/db、@n8n/permissions；本地:无。导出:SourceControlContext。关键函数/方法:hasAccessToAllProjects。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/source-control.ee/types/source-control-context.ts -> services/n8n/application/cli/services/modules/source-control.ee/types/source_control_context.py

import type { User } from '@n8n/db';
import { hasGlobalScope } from '@n8n/permissions';

export class SourceControlContext {
	constructor(private readonly userInternal: User) {}

	get user() {
		return this.userInternal;
	}

	hasAccessToAllProjects() {
		return hasGlobalScope(this.userInternal, 'project:update');
	}
}
