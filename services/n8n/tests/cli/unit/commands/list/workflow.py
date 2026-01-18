"""
MIGRATION-META:
  source_path: packages/cli/src/commands/list/workflow.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/commands/list 的工作流模块。导入/依赖:外部:zod；内部:@n8n/db、@n8n/decorators、@n8n/di；本地:../base-command。导出:ListWorkflowCommand。关键函数/方法:run。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/commands/list/workflow.ts -> services/n8n/tests/cli/unit/commands/list/workflow.py

import { WorkflowRepository } from '@n8n/db';
import { Command } from '@n8n/decorators';
import { Container } from '@n8n/di';
import { z } from 'zod';

import { BaseCommand } from '../base-command';

const flagsSchema = z.object({
	active: z
		.string()
		.describe('Filters workflows by active status. Can be true or false')
		.optional(),
	onlyId: z.boolean().describe('Outputs workflow IDs only, one per line.').default(false),
});

@Command({
	name: 'list:workflow',
	description: 'List workflows',
	examples: ['', '--active=true --onlyId', '--active=false'],
	flagsSchema,
})
export class ListWorkflowCommand extends BaseCommand<z.infer<typeof flagsSchema>> {
	async run() {
		const { flags } = this;

		if (flags.active !== undefined && !['true', 'false'].includes(flags.active)) {
			this.error('The --active flag has to be passed using true or false');
		}

		const workflowRepository = Container.get(WorkflowRepository);

		const workflows =
			flags.active !== undefined
				? await workflowRepository.findByActiveState(flags.active === 'true')
				: await workflowRepository.find();

		if (flags.onlyId) {
			workflows.forEach((workflow) => this.logger.info(workflow.id));
		} else {
			workflows.forEach((workflow) => this.logger.info(`${workflow.id}|${workflow.name}`));
		}
	}

	async catch(error: Error) {
		this.logger.error('\nGOT ERROR');
		this.logger.error('====================================');
		this.logger.error(error.message);
		this.logger.error(error.stack!);
	}
}
