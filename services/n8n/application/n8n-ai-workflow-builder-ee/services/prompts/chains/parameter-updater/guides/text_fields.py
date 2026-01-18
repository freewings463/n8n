"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater/guides/text-fields.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater 的工作流模块。导入/依赖:外部:无；内部:无；本地:../types。导出:TEXT_FIELDS_GUIDE。关键函数/方法:hasTextFields。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater/guides/text-fields.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/prompts/chains/parameter-updater/guides/text_fields.py

import type { NodeTypeGuide } from '../types';

/**
 * Checks if a node has text/string fields that might use expressions.
 */
function hasTextFields(nodeDefinition: {
	properties?: Array<{ type: string; typeOptions?: { multipleValues?: boolean } }>;
}): boolean {
	if (!nodeDefinition.properties) return false;

	return nodeDefinition.properties.some(
		(prop) => prop.type === 'string' && prop.typeOptions?.multipleValues !== true,
	);
}

export const TEXT_FIELDS_GUIDE: NodeTypeGuide = {
	patterns: ['*'],
	condition: (ctx) => hasTextFields(ctx.nodeDefinition),
	content: `
## Text Field Expression Formatting

### PREFERRED METHOD: Embedding expressions directly within text
\`\`\`
"text": "=ALERT: It is currently {{ $('Weather Node').item.json.weather }} in {{ $('Weather Node').item.json.city }}!"
\`\`\`

### Alternative method: Using string concatenation (use only when needed)
\`\`\`
"text": "={{ 'ALERT: It is currently ' + $('Weather Node').item.json.weather + ' in ' + $('Weather Node').item.json.city + '!' }}"
\`\`\`

### Key Points:
- Use the embedded expression format when mixing static text with dynamic values
- The entire string must start with = when using expressions
- Expressions within text use single curly braces {{ }}
- The outer expression wrapper uses double curly braces ={{ }}`,
};
