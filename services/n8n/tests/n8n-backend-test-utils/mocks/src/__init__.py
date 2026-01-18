"""
MIGRATION-META:
  source_path: packages/@n8n/backend-test-utils/src/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/backend-test-utils/src 的入口。导入/依赖:外部:jest-mock-extended；内部:@n8n/backend-common；本地:无。再导出:./random、./db/workflows、./db/projects、./mocking 等1项。导出:mockLogger。关键函数/方法:mockLogger。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Test utilities package -> tests/mocks
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/backend-test-utils/src/index.ts -> services/n8n/tests/n8n-backend-test-utils/mocks/src/__init__.py

import type { Logger } from '@n8n/backend-common';
import { mock } from 'jest-mock-extended';

export const mockLogger = (): Logger =>
	mock<Logger>({ scoped: jest.fn().mockReturnValue(mock<Logger>()) });

export * from './random';
export * as testDb from './test-db';
export * as testModules from './test-modules';
export * from './db/workflows';
export * from './db/projects';
export * from './mocking';
export * from './migration-test-helpers';
