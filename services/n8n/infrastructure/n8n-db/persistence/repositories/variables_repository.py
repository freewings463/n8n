"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/repositories/variables.repository.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/repositories 的仓储。导入/依赖:外部:无；内部:@n8n/di、@n8n/typeorm；本地:../entities。导出:VariablesRepository。关键函数/方法:deleteByIds。用于封装该模块数据读写与查询细节，隔离持久层。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected TypeORM Repository/EntityManager usage
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/repositories/variables.repository.ts -> services/n8n/infrastructure/n8n-db/persistence/repositories/variables_repository.py

import { Service } from '@n8n/di';
import { DataSource, In, Repository } from '@n8n/typeorm';

import { Variables } from '../entities';

@Service()
export class VariablesRepository extends Repository<Variables> {
	constructor(dataSource: DataSource) {
		super(Variables, dataSource.manager);
	}

	async deleteByIds(ids: string[]): Promise<void> {
		await this.delete({ id: In(ids) });
	}
}
