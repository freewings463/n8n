"""
MIGRATION-META:
  source_path: packages/cli/src/modules/source-control.ee/types/exportable-project.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/source-control.ee/types 的类型。导入/依赖:外部:无；内部:无；本地:./exportable-variable、./resource-owner。导出:ExportableProject、ExportableProjectWithFileName。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/source-control.ee/types/exportable-project.ts -> services/n8n/application/cli/services/modules/source-control.ee/types/exportable_project.py

import type { ExportableVariable } from './exportable-variable';
import type { TeamResourceOwner } from './resource-owner';

export interface ExportableProject {
	id: string;
	name: string;
	icon: { type: 'emoji' | 'icon'; value: string } | null;
	description: string | null;
	/**
	 * Only team projects are supported
	 */
	type: 'team';
	owner: TeamResourceOwner;
	variableStubs?: ExportableVariable[];
}

export type ExportableProjectWithFileName = ExportableProject & {
	filename: string;
};
