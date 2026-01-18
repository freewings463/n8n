"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/sqlite/1652367743993-AddUserSettings.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/sqlite 的迁移。导入/依赖:外部:无；内部:无；本地:../migration-types。导出:AddUserSettings1652367743993。关键函数/方法:up、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/sqlite/1652367743993-AddUserSettings.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/sqlite/1652367743993_AddUserSettings.py

import type { MigrationContext, ReversibleMigration } from '../migration-types';

export class AddUserSettings1652367743993 implements ReversibleMigration {
	transaction = false as const;

	async up({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(
			`CREATE TABLE "temporary_user" ("id" varchar PRIMARY KEY NOT NULL, "email" varchar(255), "firstName" varchar(32), "lastName" varchar(32), "password" varchar, "resetPasswordToken" varchar, "resetPasswordTokenExpiration" integer DEFAULT NULL, "personalizationAnswers" text, "createdAt" datetime(3) NOT NULL DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')), "updatedAt" datetime(3) NOT NULL DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')), "globalRoleId" integer NOT NULL, "settings" text, CONSTRAINT "FK_${tablePrefix}f0609be844f9200ff4365b1bb3d" FOREIGN KEY ("globalRoleId") REFERENCES "${tablePrefix}role" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION)`,
		);
		await queryRunner.query(
			`INSERT INTO "temporary_user"("id", "email", "firstName", "lastName", "password", "resetPasswordToken", "resetPasswordTokenExpiration", "personalizationAnswers", "createdAt", "updatedAt", "globalRoleId") SELECT "id", "email", "firstName", "lastName", "password", "resetPasswordToken", "resetPasswordTokenExpiration", "personalizationAnswers", "createdAt", "updatedAt", "globalRoleId" FROM "${tablePrefix}user"`,
		);
		await queryRunner.query(`DROP TABLE "${tablePrefix}user"`);
		await queryRunner.query(`ALTER TABLE "temporary_user" RENAME TO "${tablePrefix}user"`);

		await queryRunner.query(
			`CREATE UNIQUE INDEX "UQ_${tablePrefix}e12875dfb3b1d92d7d7c5377e2" ON "${tablePrefix}user" ("email")`,
		);
	}

	async down({ queryRunner, tablePrefix }: MigrationContext) {
		await queryRunner.query(`ALTER TABLE "${tablePrefix}user" RENAME TO "temporary_user"`);
		await queryRunner.query(
			`CREATE TABLE "${tablePrefix}user" ("id" varchar PRIMARY KEY NOT NULL, "email" varchar(255), "firstName" varchar(32), "lastName" varchar(32), "password" varchar, "resetPasswordToken" varchar, "resetPasswordTokenExpiration" integer DEFAULT NULL, "personalizationAnswers" text, "createdAt" datetime(3) NOT NULL DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')), "updatedAt" datetime(3) NOT NULL DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')), "globalRoleId" integer NOT NULL, CONSTRAINT "FK_${tablePrefix}f0609be844f9200ff4365b1bb3d" FOREIGN KEY ("globalRoleId") REFERENCES "${tablePrefix}role" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION)`,
		);
		await queryRunner.query(
			`INSERT INTO "${tablePrefix}user"("id", "email", "firstName", "lastName", "password", "resetPasswordToken", "resetPasswordTokenExpiration", "personalizationAnswers", "createdAt", "updatedAt", "globalRoleId") SELECT "id", "email", "firstName", "lastName", "password", "resetPasswordToken", "resetPasswordTokenExpiration", "personalizationAnswers", "createdAt", "updatedAt", "globalRoleId" FROM "temporary_user"`,
		);
		await queryRunner.query('DROP TABLE "temporary_user"');
		await queryRunner.query(
			`CREATE UNIQUE INDEX "UQ_${tablePrefix}e12875dfb3b1d92d7d7c5377e2" ON "${tablePrefix}user" ("email")`,
		);
	}
}
