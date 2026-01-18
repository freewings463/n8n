"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Webflow/V2/WebflowV2.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Webflow/V2 的节点。导入/依赖:外部:无；内部:无；本地:../GenericFunctions、./actions/router、./actions/versionDescription。导出:WebflowV2。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Webflow/V2/WebflowV2.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Webflow/V2/WebflowV2_node.py

import type {
	IExecuteFunctions,
	INodeType,
	INodeTypeBaseDescription,
	INodeTypeDescription,
} from 'n8n-workflow';

import { getSites, getCollections, getFields } from '../GenericFunctions';
import { router } from './actions/router';
import { versionDescription } from './actions/versionDescription';

export class WebflowV2 implements INodeType {
	description: INodeTypeDescription;

	constructor(baseDescription: INodeTypeBaseDescription) {
		this.description = {
			...baseDescription,
			...versionDescription,
			usableAsTool: true,
		};
	}

	methods = {
		loadOptions: {
			getSites,
			getCollections,
			getFields,
		},
	};

	async execute(this: IExecuteFunctions) {
		return await router.call(this);
	}
}
