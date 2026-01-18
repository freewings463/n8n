"""
MIGRATION-META:
  source_path: packages/cli/src/modules/source-control.ee/types/exportable-credential.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/source-control.ee/types 的类型。导入/依赖:外部:无；内部:n8n-workflow；本地:./resource-owner。导出:ExportableCredential、StatusExportableCredential。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/source-control.ee/types/exportable-credential.ts -> services/n8n/application/cli/services/modules/source-control.ee/types/exportable_credential.py

import type { ICredentialDataDecryptedObject } from 'n8n-workflow';

import type { RemoteResourceOwner, StatusResourceOwner } from './resource-owner';

export interface ExportableCredential {
	id: string;
	name: string;
	type: string;
	data: ICredentialDataDecryptedObject;

	/**
	 * Email of the user who owns this credential at the source instance.
	 * Ownership is mirrored at target instance if user is also present there.
	 */
	ownedBy: RemoteResourceOwner | null;

	/**
	 * Whether this credential is globally accessible across all projects.
	 */
	isGlobal?: boolean;
}

export type StatusExportableCredential = ExportableCredential & {
	filename: string;
	ownedBy?: StatusResourceOwner;
};
