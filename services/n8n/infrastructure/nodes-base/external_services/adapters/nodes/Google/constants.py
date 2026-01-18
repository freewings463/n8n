"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/constants.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:GOOGLE_DRIVE_FILE_URL_REGEX、GOOGLE_DRIVE_FOLDER_URL_REGEX、GOOGLE_SHEETS_SHEET_URL_REGEX。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/constants.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/constants.py

export const GOOGLE_DRIVE_FILE_URL_REGEX =
	'https:\\/\\/(?:drive|docs)\\.google\\.com(?:\\/.*|)\\/d\\/([0-9a-zA-Z\\-_]+)(?:\\/.*|)';

export const GOOGLE_DRIVE_FOLDER_URL_REGEX =
	'https:\\/\\/drive\\.google\\.com(?:\\/.*|)\\/folders\\/([0-9a-zA-Z\\-_]+)(?:\\/.*|)';

export const GOOGLE_SHEETS_SHEET_URL_REGEX =
	'https:\\/\\/docs\\.google\\.com\\/spreadsheets\\/d\\/[0-9a-zA-Z\\-_]+.*\\#gid=([0-9]+)';
