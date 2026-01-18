"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Filter/V2/FilterV2.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Filter/V2 的节点。导入/依赖:外部:lodash/set；内部:无；本地:../utils/constants、../utils/descriptions、../V2/utils。导出:FilterV2。关键函数/方法:execute、set。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Filter/V2/FilterV2.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Filter/V2/FilterV2_node.py

import set from 'lodash/set';
import {
	ApplicationError,
	NodeOperationError,
	type IExecuteFunctions,
	type INodeExecutionData,
	type INodeType,
	type INodeTypeBaseDescription,
	type INodeTypeDescription,
	NodeConnectionTypes,
} from 'n8n-workflow';

import { ENABLE_LESS_STRICT_TYPE_VALIDATION } from '../../../utils/constants';
import { looseTypeValidationProperty } from '../../../utils/descriptions';
import { getTypeValidationParameter, getTypeValidationStrictness } from '../../If/V2/utils';

export class FilterV2 implements INodeType {
	description: INodeTypeDescription;

	constructor(baseDescription: INodeTypeBaseDescription) {
		this.description = {
			...baseDescription,
			version: [2, 2.1, 2.2, 2.3],
			defaults: {
				name: 'Filter',
				color: '#229eff',
			},
			inputs: [NodeConnectionTypes.Main],
			outputs: [NodeConnectionTypes.Main],
			outputNames: ['Kept', 'Discarded'],
			parameterPane: 'wide',
			properties: [
				{
					displayName: 'Conditions',
					name: 'conditions',
					placeholder: 'Add Condition',
					type: 'filter',
					default: {},
					typeOptions: {
						filter: {
							caseSensitive: '={{!$parameter.options.ignoreCase}}',
							typeValidation: getTypeValidationStrictness(2.1),
							version: '={{ $nodeVersion >= 2.3 ? 3 : $nodeVersion >= 2.2 ? 2 : 1 }}',
						},
					},
				},
				{
					...looseTypeValidationProperty,
					default: false,
					displayOptions: {
						show: {
							'@version': [{ _cnd: { gte: 2.1 } }],
						},
					},
				},
				{
					displayName: 'Options',
					name: 'options',
					type: 'collection',
					placeholder: 'Add option',
					default: {},
					options: [
						{
							displayName: 'Ignore Case',
							description: 'Whether to ignore letter case when evaluating conditions',
							name: 'ignoreCase',
							type: 'boolean',
							default: true,
						},
						{
							...looseTypeValidationProperty,
							displayOptions: {
								show: {
									'@version': [{ _cnd: { lt: 2.1 } }],
								},
							},
						},
					],
				},
			],
		};
	}

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const keptItems: INodeExecutionData[] = [];
		const discardedItems: INodeExecutionData[] = [];

		this.getInputData().forEach((item, itemIndex) => {
			try {
				const options = this.getNodeParameter('options', itemIndex) as {
					ignoreCase?: boolean;
					looseTypeValidation?: boolean;
				};
				let pass = false;
				try {
					pass = this.getNodeParameter('conditions', itemIndex, false, {
						extractValue: true,
					}) as boolean;
				} catch (error) {
					if (
						!getTypeValidationParameter(2.1)(this, itemIndex, options.looseTypeValidation) &&
						!error.description
					) {
						set(error, 'description', ENABLE_LESS_STRICT_TYPE_VALIDATION);
					}
					set(error, 'context.itemIndex', itemIndex);
					set(error, 'node', this.getNode());
					throw error;
				}

				if (item.pairedItem === undefined) {
					item.pairedItem = { item: itemIndex };
				}

				if (pass) {
					keptItems.push(item);
				} else {
					discardedItems.push(item);
				}
			} catch (error) {
				if (this.continueOnFail()) {
					discardedItems.push(item);
				} else {
					if (error instanceof NodeOperationError) {
						throw error;
					}

					if (error instanceof ApplicationError) {
						set(error, 'context.itemIndex', itemIndex);
						throw error;
					}

					throw new NodeOperationError(this.getNode(), error, {
						itemIndex,
					});
				}
			}
		});

		return [keptItems, discardedItems];
	}
}
