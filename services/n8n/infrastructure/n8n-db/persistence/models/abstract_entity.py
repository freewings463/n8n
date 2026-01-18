"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/entities/abstract-entity.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/entities 的模块。导入/依赖:外部:无；内部:@n8n/config、@n8n/di、@n8n/typeorm、n8n-core；本地:../utils/generators。导出:jsonColumnType、datetimeColumnType、JsonColumn、DateTimeColumn、BinaryColumn、WithStringId、WithCreatedAt、WithUpdatedAt 等2项。关键函数/方法:JsonColumn、DateTimeColumn、BinaryColumn、generateId、setUpdateDate。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - DB entity -> infrastructure/persistence/models
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/entities/abstract-entity.ts -> services/n8n/infrastructure/n8n-db/persistence/models/abstract_entity.py

import { GlobalConfig } from '@n8n/config';
import { Container } from '@n8n/di';
import type { ColumnOptions } from '@n8n/typeorm';
import {
	BeforeInsert,
	BeforeUpdate,
	Column,
	CreateDateColumn,
	PrimaryColumn,
	UpdateDateColumn,
} from '@n8n/typeorm';
import type { Class } from 'n8n-core';

import { generateNanoId } from '../utils/generators';

export const { type: dbType } = Container.get(GlobalConfig).database;

const timestampSyntax = {
	sqlite: "STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')",
	postgresdb: 'CURRENT_TIMESTAMP(3)',
	mysqldb: 'CURRENT_TIMESTAMP(3)',
	mariadb: 'CURRENT_TIMESTAMP(3)',
}[dbType];

export const jsonColumnType = dbType === 'sqlite' ? 'simple-json' : 'json';
export const datetimeColumnType = dbType === 'postgresdb' ? 'timestamptz' : 'datetime';
const binaryColumnTypeMap = {
	sqlite: 'blob',
	postgresdb: 'bytea',
	mysqldb: 'longblob',
	mariadb: 'longblob',
} as const;
const binaryColumnType = binaryColumnTypeMap[dbType];

export function JsonColumn(options?: Omit<ColumnOptions, 'type'>) {
	return Column({
		...options,
		type: jsonColumnType,
	});
}

export function DateTimeColumn(options?: Omit<ColumnOptions, 'type'>) {
	return Column({
		...options,
		type: datetimeColumnType,
	});
}

export function BinaryColumn(options?: Omit<ColumnOptions, 'type'>) {
	return Column({
		...options,
		type: binaryColumnType,
	});
}

const tsColumnOptions: ColumnOptions = {
	precision: 3,
	default: () => timestampSyntax,
	type: datetimeColumnType,
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function mixinStringId<T extends Class<{}, any[]>>(base: T) {
	class Derived extends base {
		@PrimaryColumn('varchar')
		id: string;

		@BeforeInsert()
		generateId() {
			if (!this.id) {
				this.id = generateNanoId();
			}
		}
	}
	return Derived;
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function mixinUpdatedAt<T extends Class<{}, any[]>>(base: T) {
	class Derived extends base {
		@UpdateDateColumn(tsColumnOptions)
		updatedAt: Date;

		@BeforeUpdate()
		setUpdateDate(): void {
			this.updatedAt = new Date();
		}
	}
	return Derived;
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function mixinCreatedAt<T extends Class<{}, any[]>>(base: T) {
	class Derived extends base {
		@CreateDateColumn(tsColumnOptions)
		createdAt: Date;
	}
	return Derived;
}

class BaseEntity {}

export const WithStringId = mixinStringId(BaseEntity);
export const WithCreatedAt = mixinCreatedAt(BaseEntity);
export const WithUpdatedAt = mixinUpdatedAt(BaseEntity);
export const WithTimestamps = mixinCreatedAt(mixinUpdatedAt(BaseEntity));
export const WithTimestampsAndStringId = mixinStringId(WithTimestamps);
