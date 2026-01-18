"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Freshservice/constants.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Freshservice 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:LANGUAGES。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。注释目标:https://support.freshservice.com/support/solutions/articles/232303-list-of-languages-supported-in-freshservice。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Freshservice/constants.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Freshservice/constants.py

// https://support.freshservice.com/support/solutions/articles/232303-list-of-languages-supported-in-freshservice

const RAW_LANGUAGES: { [key: string]: string } = {
	en: 'English',
	ar: 'Arabic',
	ca: 'Catalan',
	cs: 'Czech',
	'cy-GB': 'Welsh',
	da: 'Danish',
	de: 'German',
	es: 'Spanish',
	'es-LA': 'Spanish (Latin America)',
	et: 'Estonian',
	fi: 'Finnish',
	fr: 'French',
	he: 'Hebrew',
	hu: 'Hungarian',
	id: 'Indonesian',
	it: 'Italian',
	'ja-JP': 'Japanese',
	ko: 'Korean',
	LV: 'Latvian',
	'nb-NO': 'Norwegian',
	nl: 'Dutch',
	pl: 'Polish',
	pt: 'Portuguese',
	'pt-BR': 'Portuguese (Brazil)',
	'pt-PT': 'Portuguese (Portugal)',
	'ru-RU': 'Russian',
	sk: 'Slovak',
	'sk-SK': 'Slovak',
	sl: 'Slovenian',
	'sv-SE': 'Swedish',
	th: 'Thai',
	tr: 'Turkish',
	UK: 'Ukrainian',
	vi: 'Vietnamese',
	'zh-CN': 'Chinese (Simplified)',
	'zh-TW': 'Chinese (Traditional)',
};

export const LANGUAGES = Object.keys(RAW_LANGUAGES).map((key) => {
	return { value: key, name: RAW_LANGUAGES[key] };
});
