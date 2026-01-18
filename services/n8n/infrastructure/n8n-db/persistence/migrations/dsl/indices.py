"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/dsl/indices.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/dsl 的迁移。导入/依赖:外部:p-lazy；内部:@n8n/typeorm；本地:无。导出:CreateIndex、DropIndex。关键函数/方法:execute。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/dsl/indices.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/dsl/indices.py

import type { QueryRunner } from '@n8n/typeorm';
import { TableIndex, TypeORMError } from '@n8n/typeorm';
import LazyPromise from 'p-lazy';

abstract class IndexOperation extends LazyPromise<void> {
	abstract execute(queryRunner: QueryRunner): Promise<void>;

	get fullTableName() {
		return [this.tablePrefix, this.tableName].join('');
	}

	get fullIndexName() {
		return ['IDX', `${this.tablePrefix}${this.tableName}`, ...this.columnNames].join('_');
	}

	constructor(
		protected tableName: string,
		protected columnNames: string[],
		protected tablePrefix: string,
		queryRunner: QueryRunner,
		protected customIndexName?: string,
	) {
		super((resolve) => {
			void this.execute(queryRunner).then(resolve);
		});
	}
}

export class CreateIndex extends IndexOperation {
	constructor(
		tableName: string,
		columnNames: string[],
		protected isUnique: boolean,
		tablePrefix: string,
		queryRunner: QueryRunner,
		customIndexName?: string,
	) {
		super(tableName, columnNames, tablePrefix, queryRunner, customIndexName);
	}

	async execute(queryRunner: QueryRunner) {
		const { columnNames, isUnique } = this;
		return await queryRunner.createIndex(
			this.fullTableName,
			new TableIndex({ name: this.customIndexName ?? this.fullIndexName, columnNames, isUnique }),
		);
	}
}

export class DropIndex extends IndexOperation {
	constructor(
		tableName: string,
		columnNames: string[],
		tablePrefix: string,
		queryRunner: QueryRunner,
		customIndexName?: string,
		protected skipIfMissing = false,
	) {
		super(tableName, columnNames, tablePrefix, queryRunner, customIndexName);
	}

	async execute(queryRunner: QueryRunner) {
		return await queryRunner
			.dropIndex(this.fullTableName, this.customIndexName ?? this.fullIndexName)
			.catch((error) => {
				if (
					error instanceof TypeORMError &&
					error.message.includes('not found') &&
					this.skipIfMissing
				) {
					return;
				}
				throw error;
			});
	}
}
