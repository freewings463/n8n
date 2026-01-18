"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/utils/test-utils/mock-entity-manager.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/utils/test-utils 的工具。导入/依赖:外部:jest-mock-extended；内部:@n8n/typeorm、n8n-core；本地:./mock-instance。导出:mockEntityManager。关键函数/方法:mockEntityManager。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected TypeORM Repository/EntityManager usage
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/utils/test-utils/mock-entity-manager.ts -> services/n8n/infrastructure/n8n-db/persistence/repositories/utils/test-utils/mock_entity_manager.py

import { DataSource, EntityManager, type EntityMetadata } from '@n8n/typeorm';
import { mock } from 'jest-mock-extended';
import type { Class } from 'n8n-core';

import { mockInstance } from './mock-instance';

export const mockEntityManager = (entityClass: Class) => {
	const entityManager = mockInstance(EntityManager);
	const dataSource = mockInstance(DataSource, {
		manager: entityManager,
		getMetadata: () => mock<EntityMetadata>({ target: entityClass }),
	});
	Object.assign(entityManager, { connection: dataSource });
	return entityManager;
};
