"""
MIGRATION-META:
  source_path: packages/cli/src/modules/data-table/data-table-ddl.service.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/modules/data-table 的服务。导入/依赖:外部:无；内部:@n8n/db、@n8n/di、@n8n/typeorm、n8n-workflow；本地:./data-table-column.entity。导出:DataTableDDLService。关键函数/方法:createTableWithColumns、dropTable、addColumn、dropColumnFromTable、renameColumn、renameColumnQuery。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected TypeORM Repository/EntityManager usage
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/data-table/data-table-ddl.service.ts -> services/n8n/infrastructure/cli/persistence/repositories/modules/data-table/data_table_ddl_service.py

import { CreateTable, DslColumn, withTransaction } from '@n8n/db';
import { Service } from '@n8n/di';
import { DataSource, DataSourceOptions, EntityManager } from '@n8n/typeorm';
import { UnexpectedError } from 'n8n-workflow';

import { DataTableColumn } from './data-table-column.entity';
import {
	addColumnQuery,
	deleteColumnQuery,
	renameColumnQuery,
	toDslColumns,
	toTableName,
} from './utils/sql-utils';

/**
 * Manages database schema operations for data tables (DDL).
 * Handles table creation, deletion, and structural modifications (columns).
 */
@Service()
export class DataTableDDLService {
	constructor(private dataSource: DataSource) {}

	async createTableWithColumns(
		dataTableId: string,
		columns: DataTableColumn[],
		trx?: EntityManager,
	) {
		await withTransaction(this.dataSource.manager, trx, async (em) => {
			if (!em.queryRunner) {
				throw new UnexpectedError('QueryRunner is not available');
			}

			const dslColumns = [new DslColumn('id').int.autoGenerate2.primary, ...toDslColumns(columns)];
			const createTable = new CreateTable(toTableName(dataTableId), '', em.queryRunner).withColumns(
				...dslColumns,
			).withTimestamps;

			await createTable.execute(em.queryRunner);
		});
	}

	async dropTable(dataTableId: string, trx?: EntityManager) {
		await withTransaction(this.dataSource.manager, trx, async (em) => {
			if (!em.queryRunner) {
				throw new UnexpectedError('QueryRunner is not available');
			}
			await em.queryRunner.dropTable(toTableName(dataTableId), true);
		});
	}

	async addColumn(
		dataTableId: string,
		column: DataTableColumn,
		dbType: DataSourceOptions['type'],
		trx?: EntityManager,
	) {
		await withTransaction(this.dataSource.manager, trx, async (em) => {
			await em.query(addColumnQuery(toTableName(dataTableId), column, dbType));
		});
	}

	async dropColumnFromTable(
		dataTableId: string,
		columnName: string,
		dbType: DataSourceOptions['type'],
		trx?: EntityManager,
	) {
		await withTransaction(this.dataSource.manager, trx, async (em) => {
			await em.query(deleteColumnQuery(toTableName(dataTableId), columnName, dbType));
		});
	}

	async renameColumn(
		dataTableId: string,
		oldColumnName: string,
		newColumnName: string,
		dbType: DataSourceOptions['type'],
		trx?: EntityManager,
	) {
		await withTransaction(this.dataSource.manager, trx, async (em) => {
			await em.query(
				renameColumnQuery(toTableName(dataTableId), oldColumnName, newColumnName, dbType),
			);
		});
	}
}
