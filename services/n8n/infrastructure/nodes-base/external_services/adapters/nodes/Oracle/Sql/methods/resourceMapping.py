"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Oracle/Sql/methods/resourceMapping.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Oracle/Sql 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../helpers/interfaces、../helpers/utils、../transport。导出:无。关键函数/方法:getMappingColumns。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Oracle/Sql/methods/resourceMapping.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Oracle/Sql/methods/resourceMapping.py

import type { ILoadOptionsFunctions, ResourceMapperFields, FieldType } from 'n8n-workflow';

import type { OracleDBNodeCredentials } from '../helpers/interfaces';
import { getColumnMetaData, mapDbType } from '../helpers/utils';
import { configureOracleDB } from '../transport';

export async function getMappingColumns(
	this: ILoadOptionsFunctions,
): Promise<ResourceMapperFields> {
	const credentials = await this.getCredentials<OracleDBNodeCredentials>('oracleDBApi');

	const pool = await configureOracleDB.call(this, credentials);

	const schema = this.getNodeParameter('schema', 0, {
		extractValue: true,
	}) as string;

	const table = this.getNodeParameter('table', 0, {
		extractValue: true,
	}) as string;

	const columns = await getColumnMetaData(this.getNode(), pool, schema, table);
	const fields = columns.map((col) => {
		const type = mapDbType(col.dataType).n8nType as FieldType;
		const nullable = col.isNullable;
		const hasDefault = col.columnDefault === 'YES';
		const isGenerated = col.isGenerated === 'ALWAYS';

		return {
			id: col.columnName,
			displayName: col.columnName,
			required: !nullable && !hasDefault && !isGenerated,
			display: true,
			type,
			defaultMatch: true,
		};
	});
	return { fields };
}
