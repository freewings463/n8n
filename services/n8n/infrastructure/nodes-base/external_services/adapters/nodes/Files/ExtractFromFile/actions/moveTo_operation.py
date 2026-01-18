"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Files/ExtractFromFile/actions/moveTo.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Files/ExtractFromFile 的节点。导入/依赖:外部:iconv-lite、lodash/set、lodash/unset、ts-ics、@utils/descriptions、@utils/utilities；内部:无；本地:无。导出:properties、description。关键函数/方法:execute、set、encoding、unset。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Files/ExtractFromFile/actions/moveTo.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Files/ExtractFromFile/actions/moveTo_operation.py

import iconv from 'iconv-lite';
import set from 'lodash/set';
import unset from 'lodash/unset';
import type {
	IDataObject,
	IExecuteFunctions,
	INodeExecutionData,
	INodeProperties,
	IBinaryData,
} from 'n8n-workflow';
import {
	BINARY_ENCODING,
	NodeOperationError,
	deepCopy,
	jsonParse,
	BINARY_MODE_COMBINED,
} from 'n8n-workflow';
import { icsCalendarToObject } from 'ts-ics';

import { encodeDecodeOptions } from '@utils/descriptions';
import { updateDisplayOptions } from '@utils/utilities';

export const properties: INodeProperties[] = [
	{
		displayName: 'Input Binary Field',
		name: 'binaryPropertyName',
		type: 'string',
		default: 'data',
		required: true,
		placeholder: 'e.g data',
		hint: 'The name of the input field containing the file data to be processed',
	},
	{
		displayName: 'Destination Output Field',
		name: 'destinationKey',
		type: 'string',
		default: 'data',
		required: true,
		placeholder: 'e.g data',
		description: 'The name of the output field that will contain the extracted data',
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add option',
		default: {},
		options: [
			{
				displayName: 'File Encoding',
				name: 'encoding',
				type: 'options',
				options: encodeDecodeOptions,
				default: 'utf8',
				description: 'Specify the encoding of the file, defaults to UTF-8',
			},
			{
				displayName: 'Strip BOM',
				name: 'stripBOM',
				displayOptions: {
					show: {
						encoding: ['utf8', 'cesu8', 'ucs2'],
					},
				},
				type: 'boolean',
				default: true,
				description:
					'Whether to strip the BOM (Byte Order Mark) from the file, this could help in an environment where the presence of the BOM is causing issues or inconsistencies',
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
		],
	},
];

const displayOptions = {
	show: {
		operation: ['binaryToPropery', 'fromJson', 'text', 'fromIcs', 'xml'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(
	this: IExecuteFunctions,
	items: INodeExecutionData[],
	operation: string,
) {
	const returnData: INodeExecutionData[] = [];
	const { binaryMode } = this.getWorkflowSettings();

	for (let itemIndex = 0; itemIndex < items.length; itemIndex++) {
		try {
			const item = items[itemIndex];
			const options = this.getNodeParameter('options', itemIndex);
			const binaryPropertyName = this.getNodeParameter('binaryPropertyName', itemIndex) as
				| string
				| IBinaryData;

			const newItem: INodeExecutionData = {
				json: {},
				pairedItem: { item: itemIndex },
			};

			const value = this.helpers.assertBinaryData(itemIndex, binaryPropertyName);

			if (!value) continue;

			const buffer = await this.helpers.getBinaryDataBuffer(itemIndex, binaryPropertyName);
			const encoding = (options.encoding as string) || this.helpers.detectBinaryEncoding(buffer);

			if (options.keepSource && options.keepSource !== 'binary') {
				newItem.json = deepCopy(item.json);
			}

			let convertedValue: string | IDataObject;
			if (operation !== 'binaryToPropery') {
				convertedValue = iconv.decode(buffer, encoding, {
					stripBOM: options.stripBOM as boolean,
				});
			} else {
				convertedValue = Buffer.from(buffer).toString(BINARY_ENCODING);
			}

			if (operation === 'fromJson') {
				if (convertedValue === '') {
					convertedValue = {};
				} else {
					convertedValue = jsonParse(convertedValue);
				}
			}

			if (operation === 'fromIcs') {
				convertedValue = icsCalendarToObject(convertedValue as string);
			}

			const destinationKey = this.getNodeParameter('destinationKey', itemIndex, '') as string;
			set(newItem.json, destinationKey, convertedValue);

			if (typeof binaryPropertyName === 'string' && binaryMode !== BINARY_MODE_COMBINED) {
				if (options.keepSource === 'binary' || options.keepSource === 'both') {
					newItem.binary = item.binary;
				} else {
					// this binary data would not be included, but there also might be other binary data
					// which should be included, copy it over and unset current binary data
					newItem.binary = deepCopy(item.binary);
					unset(newItem.binary, binaryPropertyName);
				}
			}

			returnData.push(newItem);
		} catch (error) {
			let errorDescription;
			if (typeof error.message === 'string' && error.message.includes('Unexpected token')) {
				error.message = "The file selected in 'Input Binary Field' is not in JSON format";
				errorDescription =
					"Try to change the operation or select a JSON file in 'Input Binary Field'";
			}
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
			throw new NodeOperationError(this.getNode(), error, {
				itemIndex,
				description: errorDescription,
			});
		}
	}

	return returnData;
}
