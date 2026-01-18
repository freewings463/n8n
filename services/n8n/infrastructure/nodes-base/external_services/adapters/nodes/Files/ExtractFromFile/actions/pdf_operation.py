"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Files/ExtractFromFile/actions/pdf.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Files/ExtractFromFile 的节点。导入/依赖:外部:lodash/unset、@utils/binary、@utils/utilities；内部:n8n-workflow；本地:无。导出:properties、description。关键函数/方法:execute、unset。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Files/ExtractFromFile/actions/pdf.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Files/ExtractFromFile/actions/pdf_operation.py

import unset from 'lodash/unset';
import type { IExecuteFunctions, INodeExecutionData, INodeProperties } from 'n8n-workflow';
import { NodeOperationError, deepCopy } from 'n8n-workflow';

import { extractDataFromPDF } from '@utils/binary';
import { updateDisplayOptions } from '@utils/utilities';

export const properties: INodeProperties[] = [
	{
		displayName: 'Input Binary Field',
		name: 'binaryPropertyName',
		type: 'string',
		default: 'data',
		required: true,
		placeholder: 'e.g data',
		hint: 'The name of the input binary field containing the file to be extracted',
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add option',
		default: {},
		options: [
			{
				displayName: 'Join Pages',
				name: 'joinPages',
				type: 'boolean',
				default: true,
				description:
					'Whether to join the text from all pages or return an array of text from each page',
			},
			{
				displayName: 'Keep Source',
				name: 'keepSource',
				type: 'options',
				default: 'json',
				options: [
					{
						name: 'JSON',
						value: 'json',
						description: 'Include JSON data of the input item',
					},
					{
						name: 'Binary',
						value: 'binary',
						description: 'Include binary data of the input item',
					},
					{
						name: 'Both',
						value: 'both',
						description: 'Include both JSON and binary data of the input item',
					},
				],
			},
			{
				displayName: 'Max Pages',
				name: 'maxPages',
				type: 'number',
				default: 0,
				description: 'Maximum number of pages to include',
			},
			{
				displayName: 'Password',
				name: 'password',
				type: 'string',
				typeOptions: { password: true },
				default: '',
				description: 'Prowide password, if the PDF is encrypted',
			},
		],
	},
];

const displayOptions = {
	show: {
		operation: ['pdf'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, items: INodeExecutionData[]) {
	const returnData: INodeExecutionData[] = [];

	for (let itemIndex = 0; itemIndex < items.length; itemIndex++) {
		try {
			const item = items[itemIndex];
			const options = this.getNodeParameter('options', itemIndex);
			const binaryPropertyName = this.getNodeParameter('binaryPropertyName', itemIndex);

			const json = await extractDataFromPDF.call(
				this,
				binaryPropertyName,
				options.password as string,
				options.maxPages as number,
				options.joinPages as boolean,
				itemIndex,
			);

			const newItem: INodeExecutionData = {
				json: {},
				pairedItem: { item: itemIndex },
			};

			if (options.keepSource && options.keepSource !== 'binary') {
				newItem.json = { ...deepCopy(item.json), ...json };
			} else {
				newItem.json = json;
			}

			if (options.keepSource === 'binary' || options.keepSource === 'both') {
				newItem.binary = item.binary;
			} else {
				// this binary data would not be included, but there also might be other binary data
				// which should be included, copy it over and unset current binary data
				newItem.binary = deepCopy(item.binary);
				unset(newItem.binary, binaryPropertyName);
			}

			returnData.push(newItem);
		} catch (error) {
			if (this.continueOnFail()) {
				returnData.push({
					json: {
						error: error.message,
					},
					pairedItem: {
						item: itemIndex,
					},
				});
				continue;
			}
			throw new NodeOperationError(this.getNode(), error, { itemIndex });
		}
	}

	return returnData;
}
