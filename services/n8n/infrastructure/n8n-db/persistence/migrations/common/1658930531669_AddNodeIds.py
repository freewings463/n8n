"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/migrations/common/1658930531669-AddNodeIds.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/migrations/common 的迁移。导入/依赖:外部:uuid；内部:n8n-workflow；本地:../../entities、../migration-types。导出:AddNodeIds1658930531669。关键函数/方法:up、down。用于定义该模块数据库迁移步骤（新增表/字段/索引等）。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Migration -> infrastructure/persistence/migrations
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/migrations/common/1658930531669-AddNodeIds.ts -> services/n8n/infrastructure/n8n-db/persistence/migrations/common/1658930531669_AddNodeIds.py

import type { INode } from 'n8n-workflow';
import { v4 as uuid } from 'uuid';

import type { WorkflowEntity } from '../../entities';
import type { MigrationContext, ReversibleMigration } from '../migration-types';

type Workflow = Pick<WorkflowEntity, 'id'> & { nodes: string | INode[] };

export class AddNodeIds1658930531669 implements ReversibleMigration {
	async up({ escape, runQuery, runInBatches, parseJson }: MigrationContext) {
		const tableName = escape.tableName('workflow_entity');
		const workflowsQuery = `SELECT id, nodes FROM ${tableName}`;
		await runInBatches<Workflow>(workflowsQuery, async (workflows) => {
			workflows.forEach(async (workflow) => {
				const nodes = parseJson(workflow.nodes);
				nodes.forEach((node: INode) => {
					if (!node.id) {
						node.id = uuid();
					}
				});

				await runQuery(`UPDATE ${tableName} SET nodes = :nodes WHERE id = :id`, {
					nodes: JSON.stringify(nodes),
					id: workflow.id,
				});
			});
		});
	}

	async down({ escape, runQuery, runInBatches, parseJson }: MigrationContext) {
		const tableName = escape.tableName('workflow_entity');
		const workflowsQuery = `SELECT id, nodes FROM ${tableName}`;
		await runInBatches<Workflow>(workflowsQuery, async (workflows) => {
			workflows.forEach(async (workflow) => {
				const nodes = parseJson(workflow.nodes).map(({ id, ...rest }) => rest);
				await runQuery(`UPDATE ${tableName} SET nodes = :nodes WHERE id = :id`, {
					nodes: JSON.stringify(nodes),
					id: workflow.id,
				});
			});
		});
	}
}
