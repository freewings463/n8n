"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/template/templates/shared/default/.prettierrc.js
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/template/templates/shared 的模块。导入/依赖:外部:无；内部:无；本地:无。导出:无。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - node-cli templates -> infrastructure/configuration/tooling/templates
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/template/templates/shared/default/.prettierrc.js -> services/n8n/infrastructure/n8n-node-cli/configuration/tooling/templates/templates/shared/default/_prettierrc.py

module.exports = {
	/**
	 * https://prettier.io/docs/en/options.html#semicolons
	 */
	semi: true,

	/**
	 * https://prettier.io/docs/en/options.html#trailing-commas
	 */
	trailingComma: 'all',

	/**
	 * https://prettier.io/docs/en/options.html#bracket-spacing
	 */
	bracketSpacing: true,

	/**
	 * https://prettier.io/docs/en/options.html#tabs
	 */
	useTabs: true,

	/**
	 * https://prettier.io/docs/en/options.html#tab-width
	 */
	tabWidth: 2,

	/**
	 * https://prettier.io/docs/en/options.html#arrow-function-parentheses
	 */
	arrowParens: 'always',

	/**
	 * https://prettier.io/docs/en/options.html#quotes
	 */
	singleQuote: true,

	/**
	 * https://prettier.io/docs/en/options.html#quote-props
	 */
	quoteProps: 'as-needed',

	/**
	 * https://prettier.io/docs/en/options.html#end-of-line
	 */
	endOfLine: 'lf',

	/**
	 * https://prettier.io/docs/en/options.html#print-width
	 */
	printWidth: 100,
};
