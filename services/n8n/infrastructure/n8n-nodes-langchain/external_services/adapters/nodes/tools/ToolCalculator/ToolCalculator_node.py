"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/tools/ToolCalculator/ToolCalculator.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/tools/ToolCalculator 的节点。导入/依赖:外部:@langchain/community/…/calculator、@utils/logWrapper、@utils/sharedFields；内部:无；本地:无。导出:ToolCalculator。关键函数/方法:execute、getTool、supplyData。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/tools/ToolCalculator/ToolCalculator.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/tools/ToolCalculator/ToolCalculator_node.py

import { Calculator } from '@langchain/community/tools/calculator';
import {
	type IExecuteFunctions,
	type INodeExecutionData,
	NodeConnectionTypes,
	type INodeType,
	type INodeTypeDescription,
	type ISupplyDataFunctions,
	type SupplyData,
} from 'n8n-workflow';

import { logWrapper } from '@utils/logWrapper';
import { getConnectionHintNoticeField } from '@utils/sharedFields';

function getTool(ctx: ISupplyDataFunctions | IExecuteFunctions): Calculator {
	const calculator = new Calculator();
	calculator.name = ctx.getNode().name;
	return calculator;
}

export class ToolCalculator implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Calculator',
		name: 'toolCalculator',
		icon: 'fa:calculator',
		iconColor: 'black',
		group: ['transform'],
		version: 1,
		description: 'Make it easier for AI agents to perform arithmetic',
		defaults: {
			name: 'Calculator',
		},
		codex: {
			categories: ['AI'],
			subcategories: {
				AI: ['Tools'],
				Tools: ['Other Tools'],
			},
			resources: {
				primaryDocumentation: [
					{
						url: 'https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.toolcalculator/',
					},
				],
			},
		},

		inputs: [],

		outputs: [NodeConnectionTypes.AiTool],
		outputNames: ['Tool'],
		properties: [getConnectionHintNoticeField([NodeConnectionTypes.AiAgent])],
	};

	async supplyData(this: ISupplyDataFunctions): Promise<SupplyData> {
		return {
			response: logWrapper(getTool(this), this),
		};
	}

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const calculator = getTool(this);
		const input = this.getInputData();
		const response: INodeExecutionData[] = [];
		for (let i = 0; i < input.length; i++) {
			const inputItem = input[i];
			const result = await calculator.invoke(inputItem.json);
			response.push({
				json: {
					response: result,
				},
				pairedItem: {
					item: i,
				},
			});
		}

		return [response];
	}
}
