"""
MIGRATION-META:
  source_path: packages/@n8n/backend-common/src/utils/path-util.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/backend-common/src/utils 的工具。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:isContainedWithin、safeJoinPath。关键函数/方法:isContainedWithin、safeJoinPath。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/backend-common treated as infrastructure configuration/runtime environment
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/backend-common/src/utils/path-util.ts -> services/n8n/infrastructure/n8n-backend-common/configuration/utils/path_util.py

import { UnexpectedError } from 'n8n-workflow';
import * as path from 'node:path';

/**
 * Checks if the given childPath is contained within the parentPath. Resolves
 * the paths before comparing them, so that relative paths are also supported.
 */
export function isContainedWithin(parentPath: string, childPath: string): boolean {
	parentPath = path.resolve(parentPath);
	childPath = path.resolve(childPath);

	if (parentPath === childPath) {
		return true;
	}

	return childPath.startsWith(parentPath + path.sep);
}

/**
 * Joins the given paths to the parentPath, ensuring that the resulting path
 * is still contained within the parentPath. If not, it throws an error to
 * prevent path traversal vulnerabilities.
 *
 * @throws {UnexpectedError} If the resulting path is not contained within the parentPath.
 */
export function safeJoinPath(parentPath: string, ...paths: string[]): string {
	const candidate = path.join(parentPath, ...paths);

	if (!isContainedWithin(parentPath, candidate)) {
		throw new UnexpectedError(
			`Path traversal detected, refusing to join paths: ${parentPath} and ${JSON.stringify(paths)}`,
		);
	}

	return candidate;
}
