"""
MIGRATION-META:
  source_path: packages/testing/playwright/utils/path-helper.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/utils 的工具。导入/依赖:外部:无；内部:无；本地:../Types。导出:findPackagesRoot、resolveFromRoot。关键函数/方法:findProjectRoot、findPackagesRoot、resolveFromRoot。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected runtime IO/external interaction -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/utils/path-helper.ts -> services/n8n/infrastructure/testing/container/playwright/utils/path_helper.py

import * as fs from 'fs';
import * as path from 'path';

import { TestError } from '../Types';

/**
 * Finds the project root by searching upwards for a marker file.
 * @param marker The file that identifies the project root (e.g., 'playwright.config.ts' or 'package.json').
 * @returns The absolute path to the project root.
 */
function findProjectRoot(marker: string): string {
	let dir = __dirname;
	while (!fs.existsSync(path.join(dir, marker))) {
		const parentDir = path.dirname(dir);
		if (parentDir === dir) {
			throw new TestError('Could not find project root');
		}
		dir = parentDir;
	}
	return dir;
}

/**
 * Finds a folder root by searching upwards for a marker folder named 'packages'.
 * @returns The absolute path to the folder root.
 */
export function findPackagesRoot(marker: string): string {
	let dir = __dirname;
	while (!fs.existsSync(path.join(dir, marker))) {
		const parentDir = path.dirname(dir);
		if (parentDir === dir) {
			throw new TestError('Could not find packages root');
		}
		dir = parentDir;
	}
	return dir;
}

const playwrightRoot = findProjectRoot('playwright.config.ts');

/**
 * Resolves a path relative to the Playwright project root.
 * @param pathSegments Segments of the path starting from the project root.
 * @returns An absolute path to the file or directory.
 */
export function resolveFromRoot(...pathSegments: string[]): string {
	return path.join(playwrightRoot, ...pathSegments);
}
