"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Rundeck/Rundeck.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Rundeck 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./RundeckApi。导出:Rundeck。关键函数/方法:execute、rundeckArguments。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Rundeck/Rundeck.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Rundeck/Rundeck_node.py

import type {
	IExecuteFunctions,
	IDataObject,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
} from 'n8n-workflow';
import { NodeConnectionTypes, NodeOperationError } from 'n8n-workflow';

import { RundeckApi } from './RundeckApi';

export class Rundeck implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Rundeck',
		name: 'rundeck',
		// eslint-disable-next-line n8n-nodes-base/node-class-description-icon-not-svg
		icon: 'file:rundeck.png',
		group: ['transform'],
		version: 1,
		subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
		description: 'Manage Rundeck API',
		defaults: {
			name: 'Rundeck',
		},
		usableAsTool: true,
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'rundeckApi',
				required: true,
			},
		],
		properties: [
			{
				displayName: 'Resource',
				name: 'resource',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Job',
						value: 'job',
					},
				],
				default: 'job',
			},
			{
				displayName: 'Operation',
				name: 'operation',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Execute',
						value: 'execute',
						description: 'Execute a job',
						action: 'Execute a job',
					},
					{
						name: 'Get Metadata',
						value: 'getMetadata',
						description: 'Get metadata of a job',
						action: 'Get metadata of a job',
					},
				],
				default: 'execute',
			},

			// ----------------------------------
			//         job:execute
			// ----------------------------------
			{
				displayName: 'Job ID',
				name: 'jobid',
				type: 'string',
				displayOptions: {
					show: {
						operation: ['execute'],
						resource: ['job'],
					},
				},
				default: '',
				placeholder: 'Rundeck Job ID',
				required: true,
				description: 'The job ID to execute',
			},
			{
				displayName: 'Arguments',
				name: 'arguments',
				placeholder: 'Add Argument',
				type: 'fixedCollection',
				typeOptions: {
					multipleValues: true,
				},
				displayOptions: {
					show: {
						operation: ['execute'],
						resource: ['job'],
					},
				},
				default: {},
				options: [
					{
						name: 'arguments',
						displayName: 'Arguments',
						values: [
							{
								displayName: 'Name',
								name: 'name',
								type: 'string',
								default: '',
							},
							{
								displayName: 'Value',
								name: 'value',
								type: 'string',
								default: '',
							},
						],
					},
				],
			},
			{
				displayName: 'Filter',
				name: 'filter',
				type: 'string',
				displayOptions: {
					show: {
						operation: ['execute'],
						resource: ['job'],
					},
				},
				default: '',
				placeholder: 'Add Filters',
				description: 'Filter Rundeck nodes by name',
			},

			// ----------------------------------
			//         job:getMetadata
			// ----------------------------------
			{
				displayName: 'Job ID',
				name: 'jobid',
				type: 'string',
				displayOptions: {
					show: {
						operation: ['getMetadata'],
						resource: ['job'],
					},
				},
				default: '',
				placeholder: 'Rundeck Job ID',
				required: true,
				description: 'The job ID to get metadata off',
			},
		],
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		// Input data
		const items = this.getInputData();
		const returnData: IDataObject[] = [];
		const length = items.length;

		const operation = this.getNodeParameter('operation', 0);
		const resource = this.getNodeParameter('resource', 0);
		const rundeckApi = new RundeckApi(this);
		await rundeckApi.init();

		for (let i = 0; i < length; i++) {
			if (resource === 'job') {
				if (operation === 'execute') {
					// ----------------------------------
					//         job: execute
					// ----------------------------------
					const jobid = this.getNodeParameter('jobid', i) as string;
					const rundeckArguments = (this.getNodeParameter('arguments', i) as IDataObject)
						.arguments as IDataObject[];
					const filter = this.getNodeParameter('filter', i) as string;
					const response = await rundeckApi.executeJob(jobid, rundeckArguments, filter);

					returnData.push(response);
				} else if (operation === 'getMetadata') {
					// ----------------------------------
					//         job: getMetadata
					// ----------------------------------
					const jobid = this.getNodeParameter('jobid', i) as string;
					const response = await rundeckApi.getJobMetadata(jobid);

					returnData.push(response);
				} else {
					throw new NodeOperationError(
						this.getNode(),
						`The operation "${operation}" is not supported!`,
						{ itemIndex: i },
					);
				}
			} else {
				throw new NodeOperationError(
					this.getNode(),
					`The resource "${resource}" is not supported!`,
					{ itemIndex: i },
				);
			}
		}

		return [this.helpers.returnJsonArray(returnData)];
	}
}
