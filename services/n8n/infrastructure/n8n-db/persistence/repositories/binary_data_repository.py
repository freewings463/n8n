"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/repositories/binary-data.repository.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/repositories 的仓储。导入/依赖:外部:无；内部:@n8n/config、@n8n/di、@n8n/typeorm；本地:../entities、../entities/abstract-entity。导出:BinaryDataRepository。关键函数/方法:copyStoredFile、getTableName、getColumnName。用于封装该模块数据读写与查询细节，隔离持久层。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected TypeORM Repository/EntityManager usage
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/repositories/binary-data.repository.ts -> services/n8n/infrastructure/n8n-db/persistence/repositories/binary_data_repository.py

import { DatabaseConfig } from '@n8n/config';
import { Service } from '@n8n/di';
import { DataSource, Repository } from '@n8n/typeorm';

import { BinaryDataFile } from '../entities';
import { dbType } from '../entities/abstract-entity';

@Service()
export class BinaryDataRepository extends Repository<BinaryDataFile> {
	constructor(
		dataSource: DataSource,
		private readonly databaseConfig: DatabaseConfig,
	) {
		super(BinaryDataFile, dataSource.manager);
	}

	async copyStoredFile(
		sourceFileId: string,
		targetFileId: string,
		targetSourceType: string,
		targetSourceId: string,
	): Promise<boolean> {
		const tableName = this.getTableName('binary_data');
		const fileId = this.getColumnName('fileId');
		const sourceType = this.getColumnName('sourceType');
		const sourceId = this.getColumnName('sourceId');
		const data = this.getColumnName('data');
		const mimeType = this.getColumnName('mimeType');
		const fileName = this.getColumnName('fileName');
		const fileSize = this.getColumnName('fileSize');

		const [first, second, third, fourth] =
			dbType === 'postgresdb' ? ['$1', '$2', '$3', '$4'] : ['?', '?', '?', '?'];

		const query = `
			INSERT INTO ${tableName} (${fileId}, ${sourceType}, ${sourceId}, ${data}, ${mimeType}, ${fileName}, ${fileSize})
			SELECT ${first}, ${second}, ${third}, ${data}, ${mimeType}, ${fileName}, ${fileSize}
			FROM ${tableName}
			WHERE ${fileId} = ${fourth}
		`;

		const args = [targetFileId, targetSourceType, targetSourceId, sourceFileId];

		await this.query(query, args);

		return await this.existsBy({ fileId: targetFileId });
	}

	private getTableName(name: string): string {
		const { tablePrefix } = this.databaseConfig;
		return this.manager.connection.driver.escape(`${tablePrefix}${name}`);
	}

	private getColumnName(name: string): string {
		return this.manager.connection.driver.escape(name);
	}
}
