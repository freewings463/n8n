"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/Guardrails/actions/checks/keywords.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/Guardrails/actions 的节点。导入/依赖:外部:无；内部:无；本地:../types。导出:createKeywordsCheckFn。关键函数/方法:isWordChar、keywordsCheck。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。注释目标:Source: https://github.com/openai/openai-guardrails-js/blob/b9b99b4fb454f02a362c2836aec6285176ec40a8/src/checks/keywords.ts。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/Guardrails/actions/checks/keywords.ts -> services/n8n/tests/n8n-nodes-langchain/unit/nodes/Guardrails/actions/checks/keywords.py

// Source: https://github.com/openai/openai-guardrails-js/blob/b9b99b4fb454f02a362c2836aec6285176ec40a8/src/checks/keywords.ts
import type { CreateCheckFn, GuardrailResult } from '../types';

interface KeywordsConfig {
	keywords: string[];
}

// \p{L}|\p{N}|_ - any unicode letter, number, or underscore. Alternative to \b
const WORD_CHAR_CLASS = '[\\p{L}\\p{N}_]';
const isWordChar = (() => {
	const wordCharRegex = new RegExp(WORD_CHAR_CLASS, 'u');
	return (char: string | undefined): boolean => {
		if (!char) return false;
		return wordCharRegex.test(char);
	};
})();

/**
 * Keywords-based content filtering guardrail.
 *
 * Checks if any of the configured keywords appear in the input text.
 * Can be configured to trigger tripwires on matches or just report them.
 *
 * @param text Input text to check
 * @param config Configuration specifying keywords and behavior
 * @returns GuardrailResult indicating if tripwire was triggered
 */
const keywordsCheck = (text: string, config: KeywordsConfig): GuardrailResult => {
	const { keywords } = config;

	// Sanitize keywords by stripping trailing punctuation
	const sanitizedKeywords = keywords.map((k: string) => k.replace(/[.,!?;:]+$/, ''));

	const keywordEntries = sanitizedKeywords
		.map((sanitized) => ({
			sanitized,
			escaped: sanitized.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'),
		}))
		.filter(({ sanitized }) => sanitized.length > 0);

	if (keywordEntries.length === 0) {
		return {
			guardrailName: 'keywords',
			tripwireTriggered: false,
			info: {
				matchedKeywords: [],
			},
		};
	}

	// Apply unicode-aware word boundaries per keyword so tokens that start/end with punctuation still match.
	const keywordPatterns = keywordEntries.map(({ sanitized, escaped }) => {
		const keywordChars = Array.from(sanitized);
		const firstChar = keywordChars[0];
		const lastChar = keywordChars[keywordChars.length - 1];
		const needsLeftBoundary = isWordChar(firstChar);
		const needsRightBoundary = isWordChar(lastChar);
		// not preceded by a word character
		const leftBoundary = needsLeftBoundary ? `(?<!${WORD_CHAR_CLASS})` : '';
		// not followed by a word character
		const rightBoundary = needsRightBoundary ? `(?!${WORD_CHAR_CLASS})` : '';
		return `${leftBoundary}${escaped}${rightBoundary}`;
	});

	const patternText = `(?:${keywordPatterns.join('|')})`;
	const pattern = new RegExp(patternText, 'giu'); // case-insensitive, global, unicode aware

	const matches: string[] = [];
	let match;
	const seen = new Set<string>();

	// Find all matches and collect unique ones (case-insensitive)
	while ((match = pattern.exec(text)) !== null) {
		const matchedText = match[0];
		if (!seen.has(matchedText.toLowerCase())) {
			matches.push(matchedText);
			seen.add(matchedText.toLowerCase());
		}
	}

	const tripwireTriggered = matches.length > 0;

	return {
		guardrailName: 'keywords',
		tripwireTriggered,
		info: {
			matchedKeywords: matches,
		},
	};
};

export const createKeywordsCheckFn: CreateCheckFn<KeywordsConfig> = (config) => (input: string) =>
	keywordsCheck(input, config);
