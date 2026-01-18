"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Merge/v3/actions/versionDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Merge/v3 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./mode、../helpers/utils。导出:versionDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。注释目标:eslint-disable n8n-nodes-base/node-filename-against-convention。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Merge/v3/actions/versionDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Merge/v3/actions/versionDescription.py

/* eslint-disable n8n-nodes-base/node-filename-against-convention */
import { NodeConnectionTypes, type INodeTypeDescription } from 'n8n-workflow';

import * as mode from './mode';
import { configuredInputs } from '../helpers/utils';

export const versionDescription: INodeTypeDescription = {
	displayName: 'Merge',
	name: 'merge',
	group: ['transform'],
	description: 'Merges data of multiple streams once data from both is available',
	version: [3, 3.1, 3.2],
	defaults: {
		name: 'Merge',
	},
	inputs: `={{(${configuredInputs})($parameter)}}`,
	outputs: [NodeConnectionTypes.Main],
	// If mode is chooseBranch data from both branches is required
	// to continue, else data from any input suffices
	requiredInputs: '={{ $parameter["mode"] === "chooseBranch" ? [0, 1] : 1 }}',
	properties: [...mode.description],
};
