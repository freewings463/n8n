"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/MySql/MySql.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/MySql 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./v1/MySqlV1.node、./v2/MySqlV2.node。导出:MySql。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/MySql/MySql.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/MySql/MySql_node.py

import type { INodeTypeBaseDescription, IVersionedNodeType } from 'n8n-workflow';
import { VersionedNodeType } from 'n8n-workflow';

import { MySqlV1 } from './v1/MySqlV1.node';
import { MySqlV2 } from './v2/MySqlV2.node';

export class MySql extends VersionedNodeType {
	constructor() {
		const baseDescription: INodeTypeBaseDescription = {
			displayName: 'MySQL',
			name: 'mySql',
			icon: { light: 'file:mysql.svg', dark: 'file:mysql.dark.svg' },
			group: ['input'],
			defaultVersion: 2.5,
			description: 'Get, add and update data in MySQL',
			parameterPane: 'wide',
		};

		const nodeVersions: IVersionedNodeType['nodeVersions'] = {
			1: new MySqlV1(baseDescription),
			2: new MySqlV2(baseDescription),
			2.1: new MySqlV2(baseDescription),
			2.2: new MySqlV2(baseDescription),
			2.3: new MySqlV2(baseDescription),
			2.4: new MySqlV2(baseDescription),
			2.5: new MySqlV2(baseDescription),
		};

		super(nodeVersions, baseDescription);
	}
}
