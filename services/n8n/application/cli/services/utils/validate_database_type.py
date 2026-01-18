"""
MIGRATION-META:
  source_path: packages/cli/src/utils/validate-database-type.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/utils 的工具。导入/依赖:外部:无；内部:无；本地:无。导出:supportedTypesForExport、supportedTypesForImport、validateDbTypeForExportEntities、validateDbTypeForImportEntities。关键函数/方法:validateDbTypeForExportEntities、validateDbTypeForImportEntities。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/utils/validate-database-type.ts -> services/n8n/application/cli/services/utils/validate_database_type.py

export const supportedTypesForExport = [
	'sqlite',
	'sqlite-pooled',
	'sqlite-memory',
	'postgres',
	'postgresql',
	'mysql',
	'mariadb',
	'mysqldb',
];

export const supportedTypesForImport = [
	'sqlite',
	'sqlite-pooled',
	'sqlite-memory',
	'postgres',
	'postgresql',
];

export function validateDbTypeForExportEntities(dbType: string) {
	if (!supportedTypesForExport.includes(dbType.toLowerCase())) {
		throw new Error(
			`Unsupported database type: ${dbType}. Supported types: ${supportedTypesForExport.join(', ')}`,
		);
	}
}

export function validateDbTypeForImportEntities(dbType: string) {
	if (!supportedTypesForImport.includes(dbType.toLowerCase())) {
		throw new Error(
			`Unsupported database type: ${dbType}. Supported types: ${supportedTypesForImport.join(', ')}`,
		);
	}
}
