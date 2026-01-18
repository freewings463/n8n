"""
MIGRATION-META:
  source_path: packages/cli/src/modules/source-control.ee/source-control-resource-helper.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/source-control.ee 的模块。导入/依赖:外部:无；内部:@n8n/api-types；本地:无。导出:filterByType、getDeletedResources、getNonDeletedResources。关键函数/方法:filterByType、filterByStatus、filterByStatusExcluding、getDeletedResources、getNonDeletedResources。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/source-control.ee/source-control-resource-helper.ts -> services/n8n/application/cli/services/modules/source-control.ee/source_control_resource_helper.py

import type { SourceControlledFile } from '@n8n/api-types';

export function filterByType(
	files: SourceControlledFile[],
	resourceType: SourceControlledFile['type'],
): SourceControlledFile[] {
	return files.filter((file) => file.type === resourceType);
}

function filterByStatus(
	files: SourceControlledFile[],
	resourceType: SourceControlledFile['type'],
	status: SourceControlledFile['status'],
): SourceControlledFile[] {
	return filterByType(files, resourceType).filter((file) => file.status === status);
}

function filterByStatusExcluding(
	files: SourceControlledFile[],
	resourceType: SourceControlledFile['type'],
	status: SourceControlledFile['status'],
): SourceControlledFile[] {
	return filterByType(files, resourceType).filter((file) => file.status !== status);
}

export function getDeletedResources(
	files: SourceControlledFile[],
	resourceType: SourceControlledFile['type'],
): SourceControlledFile[] {
	return filterByStatus(files, resourceType, 'deleted');
}

export function getNonDeletedResources(
	files: SourceControlledFile[],
	resourceType: SourceControlledFile['type'],
): SourceControlledFile[] {
	return filterByStatusExcluding(files, resourceType, 'deleted');
}
