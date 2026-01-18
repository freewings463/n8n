"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Evaluation/Evaluation/Evaluation.node.ee.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Evaluation/Evaluation 的节点。导入/依赖:外部:无；内部:无；本地:../actions/versionDescription、../methods。导出:Evaluation。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。注释目标:eslint-disable n8n-nodes-base/node-filename-against-convention。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Evaluation/Evaluation/Evaluation.node.ee.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Evaluation/Evaluation/Evaluation_node_ee.py

/* eslint-disable n8n-nodes-base/node-filename-against-convention */
import type {
	IExecuteFunctions,
	INodeType,
	INodeTypeDescription,
	INodeExecutionData,
} from 'n8n-workflow';
import { metricRequiresModelConnection } from 'n8n-workflow'; // See packages/workflow/src/evaluation-helpers.ts

import {
	setCheckIfEvaluatingProperties,
	setInputsProperties,
	setMetricsProperties,
	setOutputProperties,
	sourcePicker,
} from './Description.node';
import { authentication } from '../../Google/Sheet/v2/actions/versionDescription';
import { listSearch, loadOptions, credentialTest } from '../methods';
import {
	checkIfEvaluating,
	setMetrics,
	getInputConnectionTypes,
	getOutputConnectionTypes,
	setOutputs,
	setInputs,
} from '../utils/evaluationUtils';

export class Evaluation implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Evaluation',
		icon: 'fa:check-double',
		name: 'evaluation',
		group: ['transform'],
		version: [4.6, 4.7, 4.8],
		description: 'Runs an evaluation',
		eventTriggerDescription: '',
		subtitle: '={{$parameter["operation"]}}',
		defaults: {
			name: 'Evaluation',
			color: '#c3c9d5',
		},
		// Pass function explicitly since expression context doesn't allow imports in getInputConnectionTypes
		inputs: `={{(${getInputConnectionTypes})($parameter, ${metricRequiresModelConnection})}}`,
		outputs: `={{(${getOutputConnectionTypes})($parameter)}}`,
		credentials: [
			{
				name: 'googleApi',
				required: true,
				displayOptions: {
					show: {
						authentication: ['serviceAccount'],
						operation: ['setOutputs'],
					},
				},
				testedBy: 'googleApiCredentialTest',
			},
			{
				name: 'googleSheetsOAuth2Api',
				required: true,
				displayOptions: {
					show: {
						authentication: ['oAuth2'],
						operation: ['setOutputs'],
					},
				},
			},
		],
		properties: [
			{
				displayName: 'Operation',
				name: 'operation',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Set Inputs',
						value: 'setInputs',
					},
					{
						name: 'Set Outputs',
						value: 'setOutputs',
					},
					{
						name: 'Set Metrics',
						value: 'setMetrics',
					},
					{
						name: 'Check If Evaluating',
						value: 'checkIfEvaluating',
					},
				],
				default: 'setOutputs',
			},
			{
				...sourcePicker,
				default: 'dataTable',
				displayOptions: {
					show: { '@version': [{ _cnd: { gte: 4.8 } }], operation: ['setOutputs'] },
				},
			},
			{
				...sourcePicker,
				default: 'googleSheets',
				displayOptions: {
					show: { '@version': [{ _cnd: { lte: 4.7 } }], operation: ['setOutputs'] },
				},
			},
			{
				...authentication,
				displayOptions: {
					hide: {
						source: ['dataTable'],
					},
				},
			},
			...setInputsProperties,
			...setOutputProperties,
			...setMetricsProperties,
			...setCheckIfEvaluatingProperties,
		],
	};

	methods = { loadOptions, listSearch, credentialTest };

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const operation = this.getNodeParameter('operation', 0);

		if (operation === 'setOutputs') {
			return await setOutputs.call(this);
		} else if (operation === 'setInputs') {
			return setInputs.call(this);
		} else if (operation === 'setMetrics') {
			return await setMetrics.call(this);
		} else if (operation === 'checkIfEvaluating') {
			return await checkIfEvaluating.call(this);
		}

		throw new Error('Unsupported Operation');
	}
}
