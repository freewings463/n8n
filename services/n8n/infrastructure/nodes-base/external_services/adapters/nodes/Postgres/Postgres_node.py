"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Postgres/Postgres.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Postgres 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./v1/PostgresV1.node、./v2/PostgresV2.node。导出:Postgres。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Postgres/Postgres.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Postgres/Postgres_node.py

import type { INodeTypeBaseDescription, IVersionedNodeType } from 'n8n-workflow';
import { VersionedNodeType } from 'n8n-workflow';

import { PostgresV1 } from './v1/PostgresV1.node';
import { PostgresV2 } from './v2/PostgresV2.node';

export class Postgres extends VersionedNodeType {
	constructor() {
		const baseDescription: INodeTypeBaseDescription = {
			displayName: 'Postgres',
			name: 'postgres',
			icon: 'file:postgres.svg',
			group: ['input'],
			defaultVersion: 2.6,
			description: 'Get, add and update data in Postgres',
			parameterPane: 'wide',
		};

		const nodeVersions: IVersionedNodeType['nodeVersions'] = {
			1: new PostgresV1(baseDescription),
			2: new PostgresV2(baseDescription),
			2.1: new PostgresV2(baseDescription),
			2.2: new PostgresV2(baseDescription),
			2.3: new PostgresV2(baseDescription),
			2.4: new PostgresV2(baseDescription),
			2.5: new PostgresV2(baseDescription),
			2.6: new PostgresV2(baseDescription),
		};

		super(nodeVersions, baseDescription);
	}
}
