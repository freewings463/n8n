"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/Anthropic/helpers/baseAnalyze.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/Anthropic 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./interfaces、./utils、../transport。导出:无。关键函数/方法:baseAnalyze、response。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/Anthropic/helpers/baseAnalyze.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/Anthropic/helpers/baseAnalyze.py

import type { IExecuteFunctions, INodeExecutionData } from 'n8n-workflow';

import type { Content, MessagesResponse } from './interfaces';
import { getBaseUrl, splitByComma } from './utils';
import { apiRequest } from '../transport';

export async function baseAnalyze(
	this: IExecuteFunctions,
	i: number,
	urlsPropertyName: string,
	type: 'image' | 'document',
): Promise<INodeExecutionData[]> {
	const model = this.getNodeParameter('modelId', i, '', { extractValue: true }) as string;
	const inputType = this.getNodeParameter('inputType', i, 'url') as string;
	const text = this.getNodeParameter('text', i, '') as string;
	const simplify = this.getNodeParameter('simplify', i, true) as boolean;
	const options = this.getNodeParameter('options', i, {});
	const baseUrl = await getBaseUrl.call(this);
	const fileUrlPrefix = `${baseUrl}/v1/files/`;

	let content: Content[];
	if (inputType === 'url') {
		const urls = this.getNodeParameter(urlsPropertyName, i, '') as string;
		content = splitByComma(urls).map((url) => {
			if (url.startsWith(fileUrlPrefix)) {
				return {
					type,
					source: {
						type: 'file',
						file_id: url.replace(fileUrlPrefix, ''),
					},
				} as Content;
			} else {
				return {
					type,
					source: {
						type: 'url',
						url,
					},
				} as Content;
			}
		});
	} else {
		const binaryPropertyNames = this.getNodeParameter('binaryPropertyName', i, 'data');
		const promises = splitByComma(binaryPropertyNames).map(async (binaryPropertyName) => {
			const binaryData = this.helpers.assertBinaryData(i, binaryPropertyName);
			const buffer = await this.helpers.getBinaryDataBuffer(i, binaryPropertyName);
			const fileBase64 = buffer.toString('base64');
			return {
				type,
				source: {
					type: 'base64',
					media_type: binaryData.mimeType,
					data: fileBase64,
				},
			} as Content;
		});

		content = await Promise.all(promises);
	}

	content.push({
		type: 'text',
		text,
	});

	const body = {
		model,
		max_tokens: options.maxTokens ?? 1024,
		messages: [
			{
				role: 'user',
				content,
			},
		],
	};

	const response = (await apiRequest.call(this, 'POST', '/v1/messages', {
		body,
	})) as MessagesResponse;

	if (simplify) {
		return [
			{
				json: { content: response.content },
				pairedItem: { item: i },
			},
		];
	}

	return [
		{
			json: { ...response },
			pairedItem: { item: i },
		},
	];
}
