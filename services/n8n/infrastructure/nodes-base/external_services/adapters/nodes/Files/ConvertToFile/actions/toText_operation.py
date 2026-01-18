"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Files/ConvertToFile/actions/toText.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Files/ConvertToFile 的节点。导入/依赖:外部:@utils/binary、@utils/descriptions、@utils/utilities；内部:n8n-workflow；本地:无。导出:properties、description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Files/ConvertToFile/actions/toText.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Files/ConvertToFile/actions/toText_operation.py

import type { IExecuteFunctions, INodeExecutionData, INodeProperties } from 'n8n-workflow';
import { NodeOperationError } from 'n8n-workflow';

import type { JsonToBinaryOptions } from '@utils/binary';
import { createBinaryFromJson } from '@utils/binary';
import { encodeDecodeOptions } from '@utils/descriptions';
import { updateDisplayOptions } from '@utils/utilities';

export const properties: INodeProperties[] = [
	{
		displayName: 'Text Input Field',
		name: 'sourceProperty',
		type: 'string',
		default: '',
		required: true,
		placeholder: 'e.g data',
		requiresDataPath: 'single',
		description:
			"The name of the input field that contains a string to convert to a file. Use dot-notation for deep fields (e.g. 'level1.level2.currentKey').",
	},
	{
		displayName: 'Put Output File in Field',
		name: 'binaryPropertyName',
		type: 'string',
		default: 'data',
		required: true,
		placeholder: 'e.g data',
		hint: 'The name of the output binary field to put the file in',
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add option',
		default: {},
		options: [
			{
				displayName: 'Add Byte Order Mark (BOM)',
				description:
					'Whether to add special marker at the start of your text file. This marker helps some programs understand how to read the file correctly.',
				name: 'addBOM',
				displayOptions: {
					show: {
						encoding: ['utf8', 'cesu8', 'ucs2'],
					},
				},
				type: 'boolean',
				default: false,
			},
			{
				displayName: 'Encoding',
				name: 'encoding',
				type: 'options',
				options: encodeDecodeOptions,
				default: 'utf8',
				description: 'Choose the character set to use to encode the data',
			},
			{
				displayName: 'File Name',
				name: 'fileName',
				type: 'string',
				default: '',
				placeholder: 'e.g. myFile',
				description: 'Name of the output file',
			},
		],
	},
];

const displayOptions = {
	show: {
		operation: ['toText'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, items: INodeExecutionData[]) {
	const returnData: INodeExecutionData[] = [];

	for (let i = 0; i < items.length; i++) {
		try {
			const options = this.getNodeParameter('options', i, {});
			const binaryPropertyName = this.getNodeParameter('binaryPropertyName', i, 'data');
			const sourceProperty = this.getNodeParameter('sourceProperty', i) as string;

			const jsonToBinaryOptions: JsonToBinaryOptions = {
				sourceKey: sourceProperty,
				fileName: (options.fileName as string) || 'file.txt',
				mimeType: 'text/plain',
				dataIsBase64: false,
				encoding: options.encoding as string,
				addBOM: options.addBOM as boolean,
				itemIndex: i,
			};

			const binaryData = await createBinaryFromJson.call(this, items[i].json, jsonToBinaryOptions);

			const newItem: INodeExecutionData = {
				json: {},
				binary: {
					[binaryPropertyName]: binaryData,
				},
				pairedItem: { item: i },
			};

			returnData.push(newItem);
		} catch (error) {
			if (this.continueOnFail()) {
				returnData.push({
					json: {
						error: error.message,
					},
					pairedItem: {
						item: i,
					},
				});
				continue;
			}
			throw new NodeOperationError(this.getNode(), error, { itemIndex: i });
		}
	}

	return returnData;
}
