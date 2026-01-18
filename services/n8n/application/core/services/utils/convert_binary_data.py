"""
MIGRATION-META:
  source_path: packages/core/src/utils/convert-binary-data.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/utils 的工具。导入/依赖:外部:无；内部:@n8n/di、n8n-workflow；本地:../binary-data/binary-data.config、../utils/binary-helper-functions。导出:无。关键函数/方法:convertBinaryData。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Core utility helpers -> application/services/utils
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/utils/convert-binary-data.ts -> services/n8n/application/core/services/utils/convert_binary_data.py

import { Container } from '@n8n/di';
import type { IBinaryKeyData, IRunNodeResponse, WorkflowSettingsBinaryMode } from 'n8n-workflow';
import {
	BINARY_ENCODING,
	BINARY_IN_JSON_PROPERTY,
	BINARY_MODE_COMBINED,
	UnexpectedError,
} from 'n8n-workflow';

import { BinaryDataConfig } from '../binary-data/binary-data.config';
import { prepareBinaryData } from '../execution-engine/node-execution-context/utils/binary-helper-functions';

export async function convertBinaryData(
	workflowId: string,
	executionId: string | undefined,
	responseData: IRunNodeResponse,
	binaryMode: WorkflowSettingsBinaryMode | undefined,
) {
	const { mode } = Container.get(BinaryDataConfig);
	if (binaryMode !== BINARY_MODE_COMBINED || mode === 'default') return responseData;

	if (!responseData.data?.length) return responseData;

	for (const outputData of responseData.data) {
		for (const item of outputData) {
			if (!item.binary) continue;

			item.json = { ...item.json };
			item.binary = { ...item.binary };

			const embededBinaries: IBinaryKeyData = {};
			const jsonBinaries: IBinaryKeyData = {};

			for (const [key, value] of Object.entries(item.binary)) {
				if (value?.id) {
					jsonBinaries[key] = value;
					continue;
				}

				if (!executionId) {
					embededBinaries[key] = value;
					continue;
				}

				const buffer = Buffer.from(value.data, BINARY_ENCODING);
				const binaryData = await prepareBinaryData(
					buffer,
					executionId,
					workflowId,
					undefined,
					value?.mimeType,
				);

				if (value.fileName) {
					binaryData.fileName = value.fileName;
				}

				jsonBinaries[key] = binaryData;
			}

			const existingValue = item.json[BINARY_IN_JSON_PROPERTY] ?? {};
			if (Array.isArray(existingValue) || typeof existingValue !== 'object') {
				throw new UnexpectedError(
					`Binary data could not be converted. Item already has '${BINARY_IN_JSON_PROPERTY}' field, but value type is not an object`,
				);
			}

			if (Object.keys(jsonBinaries).length) {
				const existingJsonBinaries = existingValue as IBinaryKeyData;
				item.json[BINARY_IN_JSON_PROPERTY] = { ...existingJsonBinaries, ...jsonBinaries };
			}

			item.binary = Object.keys(embededBinaries).length ? embededBinaries : undefined;
		}
	}

	return responseData;
}
