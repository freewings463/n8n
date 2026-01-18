"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/utils/output_parsers/N8nItemListOutputParser.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/utils/output_parsers 的工具。导入/依赖:外部:@langchain/core/output_parsers；内部:无；本地:无。导出:N8nItemListOutputParser。关键函数/方法:parse、getFormatInstructions、getSchema。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Integration package defaulted to infrastructure/external_services
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/utils/output_parsers/N8nItemListOutputParser.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/utils/output_parsers/N8nItemListOutputParser.py

import { BaseOutputParser, OutputParserException } from '@langchain/core/output_parsers';

export class N8nItemListOutputParser extends BaseOutputParser<string[]> {
	lc_namespace = ['n8n-nodes-langchain', 'output_parsers', 'list_items'];

	private numberOfItems: number | undefined;

	private separator: string;

	constructor(options: { numberOfItems?: number; separator?: string }) {
		super();

		const { numberOfItems = 3, separator = '\n' } = options;

		if (numberOfItems && numberOfItems > 0) {
			this.numberOfItems = numberOfItems;
		}

		this.separator = separator;

		if (this.separator === '\\n') {
			this.separator = '\n';
		}
	}

	async parse(text: string): Promise<string[]> {
		const response = text
			.split(this.separator)
			.map((item) => item.trim())
			.filter((item) => item);

		if (this.numberOfItems && response.length < this.numberOfItems) {
			// Only error if to few items got returned, if there are to many we can autofix it
			throw new OutputParserException(
				`Wrong number of items returned. Expected ${this.numberOfItems} items but got ${response.length} items instead.`,
			);
		}

		return response.slice(0, this.numberOfItems);
	}

	getFormatInstructions(): string {
		const instructions = `Your response should be a list of ${
			this.numberOfItems ? this.numberOfItems + ' ' : ''
		}items separated by`;

		const numberOfExamples = this.numberOfItems ?? 3; // Default number of examples in case numberOfItems is not set

		const examples: string[] = [];
		for (let i = 1; i <= numberOfExamples; i++) {
			examples.push(`item${i}`);
		}

		return `${instructions} "${this.separator}" (for example: "${examples.join(this.separator)}")`;
	}

	getSchema() {
		return;
	}
}
