"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/dsl/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/dsl 的入口。导入/依赖:外部:无；内部:@n8n/typeorm；本地:./column、./indices。导出:createSchemaBuilder。关键函数/方法:createSchemaBuilder。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/dsl/index.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/dsl/__init__.py

import type { QueryRunner } from '@n8n/typeorm';

import { Column } from './column';
import { CreateIndex, DropIndex } from './indices';
import {
	AddColumns,
	AddForeignKey,
	AddNotNull,
	CreateTable,
	DropColumns,
	DropForeignKey,
	DropNotNull,
	DropTable,
} from './table';

export const createSchemaBuilder = (tablePrefix: string, queryRunner: QueryRunner) => ({
	column: (name: string) => new Column(name),
	/* eslint-disable @typescript-eslint/promise-function-async */
	// NOTE: Do not add `async` to these functions, as that messes up the lazy-evaluation of LazyPromise
	createTable: (tableName: string) => new CreateTable(tableName, tablePrefix, queryRunner),

	dropTable: (tableName: string) => new DropTable(tableName, tablePrefix, queryRunner),

	addColumns: (tableName: string, columns: Column[]) =>
		new AddColumns(tableName, columns, tablePrefix, queryRunner),
	dropColumns: (tableName: string, columnNames: string[]) =>
		new DropColumns(tableName, columnNames, tablePrefix, queryRunner),

	createIndex: (
		tableName: string,
		columnNames: string[],
		isUnique = false,
		customIndexName?: string,
	) => new CreateIndex(tableName, columnNames, isUnique, tablePrefix, queryRunner, customIndexName),

	dropIndex: (
		tableName: string,
		columnNames: string[],
		{ customIndexName, skipIfMissing }: { customIndexName?: string; skipIfMissing?: boolean } = {
			skipIfMissing: false,
		},
	) =>
		new DropIndex(tableName, columnNames, tablePrefix, queryRunner, customIndexName, skipIfMissing),

	addForeignKey: (
		tableName: string,
		columnName: string,
		reference: [string, string],
		customConstraintName?: string,
		onDelete?: 'RESTRICT' | 'CASCADE' | 'NO ACTION' | 'SET NULL',
	) =>
		new AddForeignKey(
			tableName,
			columnName,
			reference,
			tablePrefix,
			queryRunner,
			customConstraintName,
			onDelete,
		),

	dropForeignKey: (
		tableName: string,
		columnName: string,
		reference: [string, string],
		customConstraintName?: string,
	) =>
		new DropForeignKey(
			tableName,
			columnName,
			reference,
			tablePrefix,
			queryRunner,
			customConstraintName,
		),

	addNotNull: (tableName: string, columnName: string) =>
		new AddNotNull(tableName, columnName, tablePrefix, queryRunner),
	dropNotNull: (tableName: string, columnName: string) =>
		new DropNotNull(tableName, columnName, tablePrefix, queryRunner),

	/* eslint-enable */
});
