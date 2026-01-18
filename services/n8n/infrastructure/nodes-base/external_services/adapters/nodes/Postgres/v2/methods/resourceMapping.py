"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Postgres/v2/methods/resourceMapping.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Postgres/v2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../../transport、../helpers/interfaces、../helpers/utils。导出:无。关键函数/方法:mapPostgresType、getMappingColumns。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Postgres/v2/methods/resourceMapping.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Postgres/v2/methods/resourceMapping.py

import type { ILoadOptionsFunctions, ResourceMapperFields, FieldType } from 'n8n-workflow';

import { configurePostgres } from '../../transport';
import type { PostgresNodeCredentials } from '../helpers/interfaces';
import { getEnumValues, getEnums, getTableSchema, uniqueColumns } from '../helpers/utils';

const postgresTypeToFieldType = new Map(
	Object.entries({
		text: 'string',
		varchar: 'string',
		'character varying': 'string',
		character: 'string',
		char: 'string',
		integer: 'number',
		smallint: 'number',
		bigint: 'number',
		decimal: 'number',
		numeric: 'number',
		real: 'number',
		'double precision': 'number',
		smallserial: 'number',
		serial: 'number',
		bigserial: 'number',
		// eslint-disable-next-line id-denylist
		boolean: 'boolean',
		timestamp: 'dateTime',
		date: 'dateTime',
		timestampz: 'dateTime',
		'timestamp without time zone': 'dateTime',
		'timestamp with time zone': 'dateTime',
		time: 'time',
		'time without time zone': 'time',
		'time with time zone': 'time',
		json: 'object',
		jsonb: 'object',
		enum: 'options',
		ARRAY: 'array',

		// PostgreSQL extensions
		citext: 'string',
		uuid: 'string',
		geometry: 'string',
		geography: 'string',
		inet: 'string',
		cidr: 'string',
		macaddr: 'string',
		macaddr8: 'string',
		int4range: 'string',
		int8range: 'string',
		numrange: 'string',
		tsrange: 'string',
		tstzrange: 'string',
		daterange: 'string',
		tsvector: 'string',
		tsquery: 'string',
		hstore: 'object',
		ltree: 'string',
	} as const),
);

function mapPostgresType(
	postgresType: string,
	userDefinedType?: string,
	enumInfo?: Map<string, string[]>,
): FieldType {
	if (postgresType === 'USER-DEFINED' && userDefinedType) {
		if (enumInfo?.has(userDefinedType)) {
			return 'options';
		}
		return postgresTypeToFieldType.get(userDefinedType) ?? 'string';
	}

	return postgresTypeToFieldType.get(postgresType) ?? 'string';
}

export async function getMappingColumns(
	this: ILoadOptionsFunctions,
): Promise<ResourceMapperFields> {
	const credentials = await this.getCredentials<PostgresNodeCredentials>('postgres');

	const { db } = await configurePostgres.call(this, credentials);

	const schema = this.getNodeParameter('schema', 0, {
		extractValue: true,
	}) as string;

	const table = this.getNodeParameter('table', 0, {
		extractValue: true,
	}) as string;

	const operation = this.getNodeParameter('operation', 0, {
		extractValue: true,
	}) as string;

	const columns = await getTableSchema(db, schema, table, { getColumnsForResourceMapper: true });
	const unique = operation === 'upsert' ? await uniqueColumns(db, table, schema) : [];
	const enumInfo = await getEnums(db);
	const fields = columns.map((col) => {
		const canBeUsedToMatch =
			operation === 'upsert' ? unique.some((u) => u.attname === col.column_name) : true;
		const type = mapPostgresType(col.data_type, col.udt_name, enumInfo);
		const options =
			type === 'options' ? getEnumValues(enumInfo, col.udt_name as string) : undefined;
		const hasDefault = Boolean(col.column_default);
		const isGenerated =
			col.is_generated === 'ALWAYS' ||
			['ALWAYS', 'BY DEFAULT'].includes(col.identity_generation ?? '');
		const nullable = col.is_nullable === 'YES';
		return {
			id: col.column_name,
			displayName: col.column_name,
			required: !nullable && !hasDefault && !isGenerated,
			defaultMatch: (col.column_name === 'id' && canBeUsedToMatch) || false,
			display: true,
			type,
			canBeUsedToMatch,
			options,
		};
	});
	return { fields };
}
