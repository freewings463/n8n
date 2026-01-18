"""
MIGRATION-META:
  source_path: packages/workflow/src/extensions/expression-parser.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src/extensions 的工作流模块。导入/依赖:外部:无；内部:无；本地:无。导出:ExpressionText、ExpressionCode、ExpressionChunk、escapeCode、splitExpression、joinExpression。关键函数/方法:escapeCode、splitExpression、escapeTmplExpression、joinExpression。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package workflow treated as domain model & rules
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/extensions/expression-parser.ts -> services/n8n/domain/workflow/services/extensions/expression_parser.py

export interface ExpressionText {
	type: 'text';
	text: string;
}

export interface ExpressionCode {
	type: 'code';
	text: string;

	// This is to match behavior in our original expression evaluator (tmpl),
	// which has different behaviours if the last expression doesn't close itself.
	hasClosingBrackets: boolean;
}

export type ExpressionChunk = ExpressionCode | ExpressionText;

const OPEN_BRACKET = /(?<escape>\\|)(?<brackets>\{\{)/;
const CLOSE_BRACKET = /(?<escape>\\|)(?<brackets>\}\})/;

export const escapeCode = (text: string): string => {
	return text.replace('\\}}', '}}');
};

export const splitExpression = (expression: string): ExpressionChunk[] => {
	const chunks: ExpressionChunk[] = [];
	let searchingFor: 'open' | 'close' = 'open';
	let activeRegex = OPEN_BRACKET;

	let buffer = '';

	let index = 0;

	while (index < expression.length) {
		const expr = expression.slice(index);
		const res = activeRegex.exec(expr);
		// No more brackets. If it's a closing bracket
		// this is sort of valid so we accept it but mark
		// that it has no closing bracket.
		if (!res?.groups) {
			buffer += expr;
			if (searchingFor === 'open') {
				chunks.push({
					type: 'text',
					text: buffer,
				});
			} else {
				chunks.push({
					type: 'code',
					text: escapeCode(buffer),
					hasClosingBrackets: false,
				});
			}
			break;
		}
		if (res.groups.escape) {
			buffer += expr.slice(0, res.index + 3);
			index += res.index + 3;
		} else {
			buffer += expr.slice(0, res.index);

			if (searchingFor === 'open') {
				chunks.push({
					type: 'text',
					text: buffer,
				});
				searchingFor = 'close';
				activeRegex = CLOSE_BRACKET;
			} else {
				chunks.push({
					type: 'code',
					text: escapeCode(buffer),
					hasClosingBrackets: true,
				});
				searchingFor = 'open';
				activeRegex = OPEN_BRACKET;
			}

			index += res.index + 2;
			buffer = '';
		}
	}

	return chunks;
};

// Expressions only have closing brackets escaped
const escapeTmplExpression = (part: string) => {
	return part.replace('}}', '\\}}');
};

export const joinExpression = (parts: ExpressionChunk[]): string => {
	return parts
		.map((chunk) => {
			if (chunk.type === 'code') {
				return `{{${escapeTmplExpression(chunk.text)}${chunk.hasClosingBrackets ? '}}' : ''}`;
			}
			return chunk.text;
		})
		.join('');
};
