"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Notion/shared/constants.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Notion/shared 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:idExtractionRegexp、idValidationRegexp、databaseUrlExtractionRegexp、databaseUrlValidationRegexp、databasePageUrlExtractionRegexp、databasePageUrlValidationRegexp、blockUrlExtractionRegexp、blockUrlValidationRegexp。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Notion/shared/constants.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Notion/shared/constants.py

const notionIdRegexp = '[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}';

export const idExtractionRegexp = `^(${notionIdRegexp})`;
export const idValidationRegexp = `${idExtractionRegexp}.*`;

const baseUrlRegexp = '(?:https|http)://www\\.notion\\.so/(?:[a-z0-9-]{2,}/)?';

export const databaseUrlExtractionRegexp = `${baseUrlRegexp}(${notionIdRegexp})`;
export const databaseUrlValidationRegexp = `${databaseUrlExtractionRegexp}.*`;

export const databasePageUrlExtractionRegexp = `${baseUrlRegexp}(?:[a-zA-Z0-9-]{1,}-)?(${notionIdRegexp})`;
export const databasePageUrlValidationRegexp = `${databasePageUrlExtractionRegexp}.*`;

export const blockUrlExtractionRegexp = `${baseUrlRegexp}(?:[a-zA-Z0-9-]{2,}-)?(${notionIdRegexp})`;
export const blockUrlValidationRegexp = `${blockUrlExtractionRegexp}.*`;
