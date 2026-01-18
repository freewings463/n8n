"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1705429061930-DropRoleMapping.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:DropRoleMapping1705429061930。关键函数/方法:up、down、migrateUp、FROM、migrateDown。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1705429061930-DropRoleMapping.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1705429061930_DropRoleMapping.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

type Table = 'user' | 'shared_workflow' | 'shared_credentials';

const idColumns: Record<Table, string> = {
	user: 'id',
	shared_credentials: 'credentialsId',
	shared_workflow: 'workflowId',
};

const uidColumns: Record<Table, string> = {
	user: 'id',
	shared_credentials: 'userId',
	shared_workflow: 'userId',
};

const roleScopes: Record<Table, string> = {
	user: 'global',
	shared_credentials: 'credential',
	shared_workflow: 'workflow',
};

const foreignKeySuffixes: Record<Table, string> = {
	user: 'f0609be844f9200ff4365b1bb3d',
	shared_credentials: 'c68e056637562000b68f480815a',
	shared_workflow: '3540da03964527aa24ae014b780',
};

export class DropRoleMapping1705429061930 implements ReversibleMigration {
	async up(context: MigrationContext) {
		await this.migrateUp('user', context);
		await this.migrateUp('shared_workflow', context);
		await this.migrateUp('shared_credentials', context);
	}

	async down(context: MigrationContext) {
		await this.migrateDown('shared_workflow', context);
		await this.migrateDown('shared_credentials', context);
		await this.migrateDown('user', context);
	}

	private async migrateUp(
		table: Table,
		{
			dbType,
			escape,
			runQuery,
			schemaBuilder: { addNotNull, addColumns, dropColumns, dropForeignKey, column },
			tablePrefix,
		}: MigrationContext,
	) {
		await addColumns(table, [column('role').text]);

		const roleTable = escape.tableName('role');
		const tableName = escape.tableName(table);
		const idColumn = escape.columnName(idColumns[table]);
		const uidColumn = escape.columnName(uidColumns[table]);
		const roleColumnName = table === 'user' ? 'globalRoleId' : 'roleId';
		const roleColumn = escape.columnName(roleColumnName);
		const scope = roleScopes[table];
		const isMySQL = ['mariadb', 'mysqldb'].includes(dbType);
		const roleField = isMySQL ? `CONCAT('${scope}:', R.name)` : `'${scope}:' || R.name`;
		const subQuery = `
        SELECT ${roleField} as role, T.${idColumn} as id${
					table !== 'user' ? `, T.${uidColumn} as uid` : ''
				}
        FROM ${tableName} T
        LEFT JOIN ${roleTable} R
        ON T.${roleColumn} = R.id and R.scope = '${scope}'`;
		const where = `WHERE ${tableName}.${idColumn} = mapping.id${
			table !== 'user' ? ` AND ${tableName}.${uidColumn} = mapping.uid` : ''
		}`;
		const swQuery = isMySQL
			? `UPDATE ${tableName}, (${subQuery}) as mapping
            SET ${tableName}.role = mapping.role
            ${where}`
			: `UPDATE ${tableName}
            SET role = mapping.role
            FROM (${subQuery}) as mapping
            ${where}`;
		await runQuery(swQuery);

		await addNotNull(table, 'role');

		await dropForeignKey(
			table,
			roleColumnName,
			['role', 'id'],
			`FK_${tablePrefix}${foreignKeySuffixes[table]}`,
		);
		await dropColumns(table, [roleColumnName]);
	}

	private async migrateDown(
		table: Table,
		{
			dbType,
			escape,
			runQuery,
			schemaBuilder: { addNotNull, addColumns, dropColumns, addForeignKey, column },
			tablePrefix,
		}: MigrationContext,
	) {
		const roleColumnName = table === 'user' ? 'globalRoleId' : 'roleId';
		await addColumns(table, [column(roleColumnName).int]);

		const roleTable = escape.tableName('role');
		const tableName = escape.tableName(table);
		const idColumn = escape.columnName(idColumns[table]);
		const uidColumn = escape.columnName(uidColumns[table]);
		const roleColumn = escape.columnName(roleColumnName);
		const scope = roleScopes[table];
		const isMySQL = ['mariadb', 'mysqldb'].includes(dbType);
		const roleField = isMySQL ? `CONCAT('${scope}:', R.name)` : `'${scope}:' || R.name`;
		const subQuery = `
			SELECT R.id as role_id, T.${idColumn} as id${table !== 'user' ? `, T.${uidColumn} as uid` : ''}
			FROM ${tableName} T
			LEFT JOIN ${roleTable} R
			ON T.role = ${roleField} and R.scope = '${scope}'`;
		const where = `WHERE ${tableName}.${idColumn} = mapping.id${
			table !== 'user' ? ` AND ${tableName}.${uidColumn} = mapping.uid` : ''
		}`;
		const query = isMySQL
			? `UPDATE ${tableName}, (${subQuery}) as mapping
				SET ${tableName}.${roleColumn} = mapping.role_id
				${where}`
			: `UPDATE ${tableName}
				SET ${roleColumn} = mapping.role_id
				FROM (${subQuery}) as mapping
				${where}`;
		await runQuery(query);

		await addNotNull(table, roleColumnName);
		await addForeignKey(
			table,
			roleColumnName,
			['role', 'id'],
			`FK_${tablePrefix}${foreignKeySuffixes[table]}`,
		);

		await dropColumns(table, ['role']);
	}
}
