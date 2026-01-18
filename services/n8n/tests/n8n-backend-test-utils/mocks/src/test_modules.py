"""
MIGRATION-META:
  source_path: packages/@n8n/backend-test-utils/src/test-modules.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/backend-test-utils/src 的模块。导入/依赖:外部:无；内部:@n8n/backend-common、@n8n/di；本地:无。导出:无。关键函数/方法:loadModules。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Test utilities package -> tests/mocks
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/backend-test-utils/src/test-modules.ts -> services/n8n/tests/n8n-backend-test-utils/mocks/src/test_modules.py

import { ModuleRegistry } from '@n8n/backend-common';
import type { ModuleName } from '@n8n/backend-common';
import { Container } from '@n8n/di';

export async function loadModules(moduleNames: ModuleName[]) {
	await Container.get(ModuleRegistry).loadModules(moduleNames);
}
