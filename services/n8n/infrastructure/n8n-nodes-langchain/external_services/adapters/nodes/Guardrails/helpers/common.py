"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/Guardrails/helpers/common.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/Guardrails/helpers 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:splitByComma、parseRegex。关键函数/方法:splitByComma、parseRegex、regexMatch。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/Guardrails/helpers/common.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/Guardrails/helpers/common.py

export const splitByComma = (str: string) => {
	return str
		.split(',')
		.map((s) => s.trim())
		.filter((s) => s);
};

export const parseRegex = (input: string) => {
	const regexMatch = (input || '').toString().match(new RegExp('^/(.*?)/([gimusy]*)$'));

	let regex: RegExp;
	if (!regexMatch) {
		regex = new RegExp((input || '').toString());
	} else if (regexMatch.length === 1) {
		regex = new RegExp(regexMatch[1]);
	} else {
		regex = new RegExp(regexMatch[1], regexMatch[2]);
	}

	return regex;
};
