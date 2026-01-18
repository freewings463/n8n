"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/commands/new/prompts.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/node-cli/src/commands/new 的模块。导入/依赖:外部:@clack/prompts；内部:无；本地:../template/templates、../utils/prompts、../utils/validation。导出:nodeNamePrompt、nodeTypePrompt、declarativeTemplatePrompt。关键函数/方法:nodeNamePrompt、text、nodeTypePrompt、declarativeTemplatePrompt。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI package default -> presentation/cli
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/commands/new/prompts.ts -> services/n8n/presentation/n8n-node-cli/cli/commands/new/prompts.py

import { select, text } from '@clack/prompts';

import { templates } from '../../template/templates';
import { withCancelHandler } from '../../utils/prompts';
import { validateNodeName } from '../../utils/validation';

export const nodeNamePrompt = async () =>
	await withCancelHandler(
		text({
			message: "Package name (must start with 'n8n-nodes-' or '@org/n8n-nodes-')",
			placeholder: 'n8n-nodes-my-app',
			validate: validateNodeName,
			defaultValue: 'n8n-nodes-my-app',
		}),
	);

export const nodeTypePrompt = async () =>
	await withCancelHandler(
		select<'declarative' | 'programmatic'>({
			message: 'What kind of node are you building?',
			options: [
				{
					label: 'HTTP API',
					value: 'declarative',
					hint: 'Low-code, faster approval for n8n Cloud',
				},
				{
					label: 'Other',
					value: 'programmatic',
					hint: 'Programmatic node with full flexibility',
				},
			],
			initialValue: 'declarative',
		}),
	);

export const declarativeTemplatePrompt = async () =>
	await withCancelHandler(
		select<keyof typeof templates.declarative>({
			message: 'What template do you want to use?',
			options: Object.entries(templates.declarative).map(([value, template]) => ({
				value: value as keyof typeof templates.declarative,
				label: template.name,
				hint: template.description,
			})),
			initialValue: 'githubIssues',
		}),
	);
