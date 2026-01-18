"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ItemLists/V3/actions/common.descriptions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ItemLists/V3 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:disableDotNotationBoolean。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ItemLists/V3/actions/common.descriptions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/ItemLists/V3/actions/common_descriptions.py

import type { INodeProperties } from 'n8n-workflow';

export const disableDotNotationBoolean: INodeProperties = {
	displayName: 'Disable Dot Notation',
	name: 'disableDotNotation',
	type: 'boolean',
	default: false,
	description:
		'Whether to disallow referencing child fields using `parent.child` in the field name',
};
