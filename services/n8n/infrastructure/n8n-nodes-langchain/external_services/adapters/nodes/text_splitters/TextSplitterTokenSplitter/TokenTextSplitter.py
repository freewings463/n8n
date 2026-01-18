"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/text_splitters/TextSplitterTokenSplitter/TokenTextSplitter.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/text_splitters/TextSplitterTokenSplitter 的节点。导入/依赖:外部:@langchain/textsplitters、@utils/helpers、@utils/tokenizer/tiktoken、@utils/tokenizer/token-estimator、js-tiktoken；内部:无；本地:无。导出:TokenTextSplitter。关键函数/方法:lc_name、splitText。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/text_splitters/TextSplitterTokenSplitter/TokenTextSplitter.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/text_splitters/TextSplitterTokenSplitter/TokenTextSplitter.py

import type { TokenTextSplitterParams } from '@langchain/textsplitters';
import { TextSplitter } from '@langchain/textsplitters';
import { hasLongSequentialRepeat } from '@utils/helpers';
import { getEncoding } from '@utils/tokenizer/tiktoken';
import { estimateTextSplitsByTokens } from '@utils/tokenizer/token-estimator';
import type * as tiktoken from 'js-tiktoken';

/**
 * Implementation of splitter which looks at tokens.
 * This is override of the LangChain TokenTextSplitter
 * to use the n8n tokenizer utility which uses local JSON encodings
 */
export class TokenTextSplitter extends TextSplitter implements TokenTextSplitterParams {
	static lc_name() {
		return 'TokenTextSplitter';
	}

	encodingName: tiktoken.TiktokenEncoding;

	allowedSpecial: 'all' | string[];

	disallowedSpecial: 'all' | string[];

	private tokenizer: tiktoken.Tiktoken | undefined;

	constructor(fields?: Partial<TokenTextSplitterParams>) {
		super(fields);

		this.encodingName = fields?.encodingName ?? 'cl100k_base';
		this.allowedSpecial = fields?.allowedSpecial ?? [];
		this.disallowedSpecial = fields?.disallowedSpecial ?? 'all';
	}

	async splitText(text: string): Promise<string[]> {
		try {
			// Validate input
			if (!text || typeof text !== 'string') {
				return [];
			}

			// Check for repetitive content
			if (hasLongSequentialRepeat(text)) {
				const splits = estimateTextSplitsByTokens(
					text,
					this.chunkSize,
					this.chunkOverlap,
					this.encodingName,
				);
				return splits;
			}

			// Use tiktoken for normal text
			try {
				this.tokenizer ??= await getEncoding(this.encodingName);

				const splits: string[] = [];
				const input_ids = this.tokenizer.encode(text, this.allowedSpecial, this.disallowedSpecial);

				let start_idx = 0;
				let chunkCount = 0;

				while (start_idx < input_ids.length) {
					if (start_idx > 0) {
						start_idx = Math.max(0, start_idx - this.chunkOverlap);
					}
					const end_idx = Math.min(start_idx + this.chunkSize, input_ids.length);
					const chunk_ids = input_ids.slice(start_idx, end_idx);

					splits.push(this.tokenizer.decode(chunk_ids));

					chunkCount++;
					start_idx = end_idx;
				}

				return splits;
			} catch (tiktokenError) {
				// Fall back to character-based splitting if tiktoken fails
				return estimateTextSplitsByTokens(
					text,
					this.chunkSize,
					this.chunkOverlap,
					this.encodingName,
				);
			}
		} catch (error) {
			// Return empty array on complete failure
			return [];
		}
	}
}
