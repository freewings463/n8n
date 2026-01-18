"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Drive/v2/helpers/interfaces.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Drive 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:UPLOAD_CHUNK_SIZE、SearchFilter、RLC_DRIVE_DEFAULT、RLC_FOLDER_DEFAULT、DRIVE。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Drive/v2/helpers/interfaces.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Drive/v2/helpers/interfaces.py

export const UPLOAD_CHUNK_SIZE = 256 * 1024;

export type SearchFilter = {
	driveId?: {
		value: string;
		mode: string;
	};
	folderId?: {
		value: string;
		mode: string;
	};
	whatToSearch?: 'all' | 'files' | 'folders';
	fileTypes?: string[];
	includeTrashed?: boolean;
};

export const RLC_DRIVE_DEFAULT = 'My Drive';
export const RLC_FOLDER_DEFAULT = 'root';

export const DRIVE = {
	FOLDER: 'application/vnd.google-apps.folder',
	AUDIO: 'application/vnd.google-apps.audio',
	DOCUMENT: 'application/vnd.google-apps.document',
	SDK: 'application/vnd.google-apps.drive-sdk',
	DRAWING: 'application/vnd.google-apps.drawing',
	FILE: 'application/vnd.google-apps.file',
	FORM: 'application/vnd.google-apps.form',
	FUSIONTABLE: 'application/vnd.google-apps.fusiontable',
	MAP: 'application/vnd.google-apps.map',
	PHOTO: 'application/vnd.google-apps.photo',
	PRESENTATION: 'application/vnd.google-apps.presentation',
	APP_SCRIPTS: 'application/vnd.google-apps.script',
	SITES: 'application/vnd.google-apps.sites',
	SPREADSHEET: 'application/vnd.google-apps.spreadsheet',
	UNKNOWN: 'application/vnd.google-apps.unknown',
	VIDEO: 'application/vnd.google-apps.video',
} as const;
