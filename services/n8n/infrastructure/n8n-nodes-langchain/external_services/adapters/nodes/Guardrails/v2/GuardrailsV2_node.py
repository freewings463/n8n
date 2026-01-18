"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/Guardrails/v2/GuardrailsV2.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/Guardrails/v2 的节点。导入/依赖:外部:无；内部:无；本地:../actions/execute、../description、../helpers/configureNodeInputs。导出:GuardrailsV2。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/Guardrails/v2/GuardrailsV2.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/Guardrails/v2/GuardrailsV2_node.py

import {
	type INodeType,
	type INodeTypeBaseDescription,
	type INodeTypeDescription,
	type IExecuteFunctions,
	type INodeExecutionData,
	NodeConnectionTypes,
} from 'n8n-workflow';

import { execute } from '../actions/execute';
import { propertiesDescription } from '../description';
import { configureNodeInputsV2 } from '../helpers/configureNodeInputs';

export class GuardrailsV2 implements INodeType {
	description: INodeTypeDescription;

	constructor(baseDescription: INodeTypeBaseDescription) {
		this.description = {
			...baseDescription,
			version: [2],
			inputs: `={{(${configureNodeInputsV2})($parameter)}}`,
			outputs: `={{
		((parameters) => {
			const operation = parameters.operation ?? 'classify';

			if (operation === 'classify') {
				return [{displayName: "Pass", type: "${NodeConnectionTypes.Main}"}, {displayName: "Fail", type: "${NodeConnectionTypes.Main}"}]
			}

			return [{ displayName: "", type: "${NodeConnectionTypes.Main}"}]
		})($parameter)
	}}`,
			defaults: {
				name: 'Guardrails',
			},
			properties: propertiesDescription,
		};
	}

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		return await execute.call(this);
	}
}
