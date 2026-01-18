"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Html/utils.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Html 的节点。导入/依赖:外部:html-to-text；内部:n8n-workflow；本地:./types。导出:getValue。关键函数/方法:getValue。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Html/utils.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Html/utils.py

import { convert } from 'html-to-text';
import type { IDataObject } from 'n8n-workflow';

import type { IValueData, Cheerio } from './types';

// The extraction functions
const extractFunctions: {
	[key: string]: ($: Cheerio, valueData: IValueData, nodeVersion: number) => string | undefined;
} = {
	attribute: ($: Cheerio, valueData: IValueData): string | undefined =>
		$.attr(valueData.attribute!),
	html: ($: Cheerio, _valueData: IValueData): string | undefined => $.html() || undefined,
	text: ($: Cheerio, _valueData: IValueData, nodeVersion: number): string | undefined => {
		if (nodeVersion <= 1.1) return $.text() || undefined;

		const html = $.html() || '';

		let options;
		if (_valueData.skipSelectors) {
			options = {
				selectors: _valueData.skipSelectors.split(',').map((s) => ({
					selector: s.trim(),
					format: 'skip',
				})),
			};
		}
		return convert(html, options);
	},
	value: ($: Cheerio, _valueData: IValueData): string | undefined => $.val(),
};

/**
 * Simple helper function which applies options
 */
export function getValue(
	$: Cheerio,
	valueData: IValueData,
	options: IDataObject,
	nodeVersion: number,
) {
	let value = extractFunctions[valueData.returnValue]($, valueData, nodeVersion);

	if (value === undefined) {
		return value;
	}

	if (options.trimValues) {
		value = value.trim();
	}

	if (options.cleanUpText) {
		value = value
			.replace(/^\s+|\s+$/g, '')
			.replace(/(\r\n|\n|\r)/gm, '')
			.replace(/\s+/g, ' ');
	}

	return value;
}
