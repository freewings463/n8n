"""
MIGRATION-META:
  source_path: packages/@n8n/backend-test-utils/src/mocking.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/backend-test-utils/src 的模块。导入/依赖:外部:jest-mock-extended、ts-essentials；内部:@n8n/di；本地:无。导出:mockInstance。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Test utilities package -> tests/mocks
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/backend-test-utils/src/mocking.ts -> services/n8n/tests/n8n-backend-test-utils/mocks/src/mocking.py

import { Container, type Constructable } from '@n8n/di';
import { mock } from 'jest-mock-extended';
import type { DeepPartial } from 'ts-essentials';

export const mockInstance = <T>(
	serviceClass: Constructable<T>,
	data: DeepPartial<T> | undefined = undefined,
) => {
	const instance = mock<T>(data);
	Container.set(serviceClass, instance);
	return instance;
};
