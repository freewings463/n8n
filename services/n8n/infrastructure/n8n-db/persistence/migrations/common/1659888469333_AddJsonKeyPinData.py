"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1659888469333-AddJsonKeyPinData.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的迁移。导入/依赖:外部:无；内部:@n8n/backend-common、n8n-workflow；本地:../migration-types。导出:AddJsonKeyPinData1659888469333。关键函数/方法:isJsonKeyObject、up、async、makeUpdateParams。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1659888469333-AddJsonKeyPinData.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1659888469333_AddJsonKeyPinData.py

import { isObjectLiteral } from '@n8n/backend-common';
import type { IDataObject, INodeExecutionData } from 'n8n-workflow';

import type { MigrationContext, IrreversibleMigration } from '../migration-types';

type OldPinnedData = { [nodeName: string]: IDataObject[] };
type NewPinnedData = { [nodeName: string]: INodeExecutionData[] };
type Workflow = { id: number; pinData: string | OldPinnedData };

function isJsonKeyObject(item: unknown): item is {
	json: unknown;
	[keys: string]: unknown;
} {
	if (!isObjectLiteral(item)) return false;
	return Object.keys(item).includes('json');
}

/**
 * Convert TEXT-type `pinData` column in `workflow_entity` table from
 * `{ [nodeName: string]: IDataObject[] }` to `{ [nodeName: string]: INodeExecutionData[] }`
 */
export class AddJsonKeyPinData1659888469333 implements IrreversibleMigration {
	async up({ escape, runQuery, runInBatches }: MigrationContext) {
		const tableName = escape.tableName('workflow_entity');
		const columnName = escape.columnName('pinData');

		const selectQuery = `SELECT id, ${columnName} FROM ${tableName} WHERE ${columnName} IS NOT NULL`;
		await runInBatches<Workflow>(selectQuery, async (workflows) => {
			await Promise.all(
				this.makeUpdateParams(workflows).map(
					async (workflow) =>
						await runQuery(`UPDATE ${tableName} SET ${columnName} = :pinData WHERE id = :id;`, {
							pinData: workflow.pinData,
							id: workflow.id,
						}),
				),
			);
		});
	}

	private makeUpdateParams(fetchedWorkflows: Workflow[]) {
		return fetchedWorkflows.reduce<Workflow[]>((updateParams, { id, pinData: rawPinData }) => {
			let pinDataPerWorkflow: OldPinnedData | NewPinnedData;

			if (typeof rawPinData === 'string') {
				try {
					// eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
					pinDataPerWorkflow = JSON.parse(rawPinData);
				} catch {
					pinDataPerWorkflow = {};
				}
			} else {
				pinDataPerWorkflow = rawPinData;
			}

			const newPinDataPerWorkflow = Object.keys(pinDataPerWorkflow).reduce<NewPinnedData>(
				(newPinDataPerWorkflow, nodeName) => {
					let pinDataPerNode = pinDataPerWorkflow[nodeName];

					if (!Array.isArray(pinDataPerNode)) {
						pinDataPerNode = [pinDataPerNode];
					}

					if (pinDataPerNode.every((item) => item.json)) return newPinDataPerWorkflow;

					newPinDataPerWorkflow[nodeName] = pinDataPerNode.map((item) =>
						isJsonKeyObject(item) ? item : { json: item },
					);

					return newPinDataPerWorkflow;
				},
				{},
			);

			if (Object.keys(newPinDataPerWorkflow).length > 0) {
				updateParams.push({ id, pinData: JSON.stringify(newPinDataPerWorkflow) });
			}

			return updateParams;
		}, []);
	}
}
