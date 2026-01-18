"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/template/templates/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/template/templates 的入口。导入/依赖:外部:无；内部:无；本地:../custom/template、../github-issues/template、../example/template。导出:templates、TemplateMap、TemplateType、TemplateName、getTemplate、isTemplateType、isTemplateName。关键函数/方法:isTemplateType。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - node-cli templates -> infrastructure/configuration/tooling/templates
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/template/templates/index.ts -> services/n8n/infrastructure/n8n-node-cli/configuration/tooling/templates/templates/__init__.py

import { customTemplate } from './declarative/custom/template';
import { githubIssuesTemplate } from './declarative/github-issues/template';
import { exampleTemplate } from './programmatic/example/template';

export const templates = {
	declarative: {
		githubIssues: githubIssuesTemplate,
		custom: customTemplate,
	},
	programmatic: {
		example: exampleTemplate,
	},
} as const;

export type TemplateMap = typeof templates;
export type TemplateType = keyof TemplateMap;
export type TemplateName<T extends TemplateType> = keyof TemplateMap[T];

export function getTemplate<T extends TemplateType, N extends TemplateName<T>>(
	type: T,
	name: N,
): TemplateMap[T][N] {
	return templates[type][name];
}

export function isTemplateType(val: unknown): val is TemplateType {
	return typeof val === 'string' && val in templates;
}

export function isTemplateName<T extends TemplateType>(
	type: T,
	name: unknown,
): name is TemplateName<T> {
	return typeof name === 'string' && name in templates[type];
}
