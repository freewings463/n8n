"""
MIGRATION-META:
  source_path: packages/cli/src/modules/source-control.ee/constants.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/source-control.ee 的模块。导入/依赖:外部:无；内部:无；本地:无。导出:SOURCE_CONTROL_PREFERENCES_DB_KEY、SOURCE_CONTROL_GIT_FOLDER、SOURCE_CONTROL_GIT_KEY_COMMENT、SOURCE_CONTROL_WORKFLOW_EXPORT_FOLDER、SOURCE_CONTROL_PROJECT_EXPORT_FOLDER、SOURCE_CONTROL_CREDENTIAL_EXPORT_FOLDER、SOURCE_CONTROL_VARIABLES_EXPORT_FILE、SOURCE_CONTROL_TAGS_EXPORT_FILE 等9项。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/source-control.ee/constants.ts -> services/n8n/application/cli/services/modules/source-control.ee/constants.py

export const SOURCE_CONTROL_PREFERENCES_DB_KEY = 'features.sourceControl';
export const SOURCE_CONTROL_GIT_FOLDER = 'git';
export const SOURCE_CONTROL_GIT_KEY_COMMENT = 'n8n deploy key';
export const SOURCE_CONTROL_WORKFLOW_EXPORT_FOLDER = 'workflows';
export const SOURCE_CONTROL_PROJECT_EXPORT_FOLDER = 'projects';
export const SOURCE_CONTROL_CREDENTIAL_EXPORT_FOLDER = 'credential_stubs';
export const SOURCE_CONTROL_VARIABLES_EXPORT_FILE = 'variable_stubs.json';
export const SOURCE_CONTROL_TAGS_EXPORT_FILE = 'tags.json';
export const SOURCE_CONTROL_FOLDERS_EXPORT_FILE = 'folders.json';
export const SOURCE_CONTROL_OWNERS_EXPORT_FILE = 'workflow_owners.json';
export const SOURCE_CONTROL_SSH_FOLDER = 'ssh';
export const SOURCE_CONTROL_SSH_KEY_NAME = 'key';
export const SOURCE_CONTROL_DEFAULT_BRANCH = 'main';
export const SOURCE_CONTROL_ORIGIN = 'origin';
export const SOURCE_CONTROL_README = `
# n8n Source Control
`;
export const SOURCE_CONTROL_DEFAULT_NAME = 'n8n user';
export const SOURCE_CONTROL_DEFAULT_EMAIL = 'n8n@example.com';
