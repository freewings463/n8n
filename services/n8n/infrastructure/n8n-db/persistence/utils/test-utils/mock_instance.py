"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/utils/test-utils/mock-instance.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/utils/test-utils 的工具。导入/依赖:外部:jest-mock-extended、ts-essentials；内部:@n8n/di；本地:无。导出:mockInstance。关键函数/方法:无。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package @n8n/db defaulted to persistence infrastructure
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/utils/test-utils/mock-instance.ts -> services/n8n/infrastructure/n8n-db/persistence/utils/test-utils/mock_instance.py

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
