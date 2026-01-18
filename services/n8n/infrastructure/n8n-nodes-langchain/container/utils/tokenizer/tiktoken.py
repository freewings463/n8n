"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/utils/tokenizer/tiktoken.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/utils/tokenizer 的工具。导入/依赖:外部:fs/promises、js-tiktoken/lite；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:loadJSONFile、getEncoding、encodingForModel。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected runtime IO/external interaction -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/utils/tokenizer/tiktoken.ts -> services/n8n/infrastructure/n8n-nodes-langchain/container/utils/tokenizer/tiktoken.py

import { readFile } from 'fs/promises';
import type { TiktokenBPE, TiktokenEncoding, TiktokenModel } from 'js-tiktoken/lite';
import { Tiktoken, getEncodingNameForModel } from 'js-tiktoken/lite';
import { jsonParse } from 'n8n-workflow';
import { join } from 'path';

const cache: Record<string, Promise<Tiktoken>> = {};

const loadJSONFile = async (filename: string): Promise<TiktokenBPE> => {
	const filePath = join(__dirname, filename);
	const content = await readFile(filePath, 'utf-8');
	return await jsonParse(content);
};

export async function getEncoding(encoding: TiktokenEncoding): Promise<Tiktoken> {
	if (!(encoding in cache)) {
		// Create and cache the promise for loading this encoding
		cache[encoding] = (async () => {
			let jsonData: TiktokenBPE;

			switch (encoding) {
				case 'o200k_base':
					jsonData = await loadJSONFile('./o200k_base.json');
					break;
				case 'cl100k_base':
					jsonData = await loadJSONFile('./cl100k_base.json');
					break;
				default:
					// Fall back to cl100k_base for unsupported encodings
					jsonData = await loadJSONFile('./cl100k_base.json');
			}

			return new Tiktoken(jsonData);
		})().catch((error) => {
			delete cache[encoding];
			throw error;
		});
	}

	return await cache[encoding];
}

export async function encodingForModel(model: TiktokenModel): Promise<Tiktoken> {
	return await getEncoding(getEncodingNameForModel(model));
}
