"""
MIGRATION-META:
  source_path: packages/@n8n/utils/src/string/truncate.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/utils/src/string 的工具。导入/依赖:外部:无；内部:无；本地:无。导出:truncate、truncateBeforeLast。关键函数/方法:truncate、truncateBeforeLast。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Generic shared utilities -> application/services/utils
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/utils/src/string/truncate.ts -> services/n8n/application/n8n-utils/services/utils/string/truncate.py

export const truncate = (text: string, length = 30): string =>
	text.length > length ? text.slice(0, length) + '...' : text;

/**
 * Replace part of given text with ellipsis following the rules below:
 *
 * - Remove chars just before the last word, as long as the last word is under 15 chars
 * - Otherwise preserve the last 5 chars of the name and remove chars before that
 */
export function truncateBeforeLast(
	text: string,
	maxLength: number,
	lastCharsLength: number = 5,
): string {
	const chars: string[] = [];

	const segmenter = new Intl.Segmenter(undefined, { granularity: 'grapheme' });

	for (const { segment } of segmenter.segment(text)) {
		chars.push(segment);
	}

	if (chars.length <= maxLength) {
		return text;
	}

	const lastWhitespaceIndex = chars.findLastIndex((ch) => ch.match(/^\s+$/));
	const lastWordIndex = lastWhitespaceIndex + 1;
	const lastWord = chars.slice(lastWordIndex);
	const ellipsis = '…';
	const ellipsisLength = ellipsis.length;

	if (lastWord.length < 15) {
		const charsToRemove = chars.length - maxLength + ellipsisLength;
		const indexBeforeLastWord = lastWordIndex;
		const keepLength = indexBeforeLastWord - charsToRemove;

		if (keepLength > 0) {
			return (
				chars.slice(0, keepLength).join('') + ellipsis + chars.slice(indexBeforeLastWord).join('')
			);
		}
	}

	if (lastCharsLength < 1) {
		return chars.slice(0, maxLength).join('') + ellipsis;
	}

	return (
		chars.slice(0, maxLength - lastCharsLength - ellipsisLength).join('') +
		ellipsis +
		chars.slice(-lastCharsLength).join('')
	);
}
