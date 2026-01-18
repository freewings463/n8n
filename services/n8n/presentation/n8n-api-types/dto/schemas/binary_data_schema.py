"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/schemas/binary-data.schema.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/schemas 的模块。导入/依赖:外部:无；内部:无；本地:无。导出:ViewableMimeTypes。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。注释目标:List of MIME types that are considered safe to be viewed directly in a browser. / Explicitly excluded from this list:。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/schemas/binary-data.schema.ts -> services/n8n/presentation/n8n-api-types/dto/schemas/binary_data_schema.py

/**
 * List of MIME types that are considered safe to be viewed directly in a browser.
 *
 * Explicitly excluded from this list:
 * - 'text/html': Excluded due to high XSS risks, as HTML can execute arbitrary JavaScript
 * - 'image/svg+xml': Excluded because SVG can contain embedded JavaScript that might execute in certain contexts
 * - 'application/pdf': Excluded due to potential arbitrary code-execution vulnerabilities in PDF rendering engines
 */
export const ViewableMimeTypes = [
	'application/json',

	'audio/mpeg',
	'audio/ogg',
	'audio/wav',

	'image/bmp',
	'image/gif',
	'image/jpeg',
	'image/jpg',
	'image/png',
	'image/tiff',
	'image/webp',

	'text/css',
	'text/csv',
	'text/markdown',
	'text/plain',

	'video/mp4',
	'video/ogg',
	'video/webm',
];
