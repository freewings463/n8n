"""
MIGRATION-META:
  source_path: packages/@n8n/config/src/utils/utils.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/config/src/utils 的工具。导入/依赖:外部:无；内部:无；本地:无。导出:getN8nFolder。关键函数/方法:getN8nFolder。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/config treated as infrastructure configuration/runtime environment
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/config/src/utils/utils.ts -> services/n8n/infrastructure/n8n-config/configuration/utils/utils.py

import path from 'node:path';

/**
 * Computes the n8n folder path based on environment variables.
 * This is used by various configs that need to know the n8n installation directory.
 */
export function getN8nFolder(): string {
	const homeVarName = process.platform === 'win32' ? 'USERPROFILE' : 'HOME';
	const userHome = process.env.N8N_USER_FOLDER ?? process.env[homeVarName] ?? process.cwd();
	return path.join(userHome, '.n8n');
}
