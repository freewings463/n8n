"""
MIGRATION-META:
  source_path: packages/workflow/src/native-methods/number.methods.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src/native-methods 的工作流模块。导入/依赖:外部:无；内部:无；本地:../extensions/extensions。导出:numberMethods。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package workflow treated as domain model & rules
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/native-methods/number.methods.ts -> services/n8n/domain/workflow/services/native-methods/number_methods.py

import type { NativeDoc } from '../extensions/extensions';

export const numberMethods: NativeDoc = {
	typeName: 'Number',
	functions: {
		toFixed: {
			doc: {
				name: 'toFixed',
				hidden: true,
				description:
					'Formats a number using fixed-point notation. `digits` defaults to null if not given.',
				docURL:
					'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/toFixed',
				returnType: 'string',
				args: [{ name: 'digits?', type: 'number' }],
			},
		},
		toPrecision: {
			doc: {
				name: 'toPrecision',
				hidden: true,
				description: 'Returns a string representing the number to the specified precision.',
				docURL:
					'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/toPrecision',
				returnType: 'string',
				args: [{ name: 'precision?', type: 'number' }],
			},
		},
		toString: {
			doc: {
				name: 'toString',
				description:
					'Converts the number to a string. For more formatting options, see <code>toLocaleString()</code>.',
				examples: [
					{ example: '(2).toString()', evaluated: "'2'" },
					{ example: '(50.125).toString()', evaluated: "'50.125'" },
					{ example: '(5).toString(2)', evaluated: "'101'" },
					{ example: '(412).toString(16)', evaluated: "'19c'" },
				],
				docURL:
					'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/toString',
				args: [
					{
						name: 'base',
						optional: true,
						description:
							'The base to use. Must be an integer between 2 and 36. E.g. base <code>2</code> is binary and base <code>16</code> is hexadecimal.',
						default: '10',
						type: 'number',
					},
				],
				returnType: 'string',
			},
		},
		toLocaleString: {
			doc: {
				name: 'toLocaleString',
				description:
					"Returns a localized string representing the number, i.e. in the language and format corresponding to its locale. Defaults to the system's locale if none specified.",
				examples: [
					{
						example: '(500000.125).toLocaleString()',
						evaluated: "'500,000.125' (if in US English locale)",
					},
					{ example: "(500000.125).toLocaleString('fr-FR')", evaluated: "'500 000,125'" },
					{
						example: "(500000.125).toLocaleString('fr-FR', {style:'currency', currency:'EUR'})",
						evaluated: "'500 000,13 €'",
					},
				],
				docURL:
					'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/toLocaleString',
				args: [
					{
						name: 'locale(s)',
						optional: true,
						description:
							'The locale to use, e.g. \'en-GB\' for British English or \'pt-BR\' for Brazilian Portuguese. See <a target="_blank" href="https://www.localeplanet.com/icu/">full list</a> (unofficial). Also accepts an <a target="_blank" href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl#locales_argument">array of locales</a>. Defaults to the system locale if not specified.',
						type: 'string | string[]',
					},
					{
						name: 'options',
						optional: true,
						description:
							'An object with <a target="_blank" href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat/NumberFormat#parameters">formatting options</a>',
						type: 'object',
					},
				],
				returnType: 'string',
			},
		},
	},
};
