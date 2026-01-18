"""
MIGRATION-META:
  source_path: packages/cli/src/commands/unpublish/workflow.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/commands/unpublish 的工作流模块。导入/依赖:外部:zod；内部:@n8n/db、@n8n/decorators、@n8n/di；本地:../base-command。导出:UnpublishWorkflowCommand。关键函数/方法:run。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/commands/unpublish/workflow.ts -> services/n8n/tests/cli/unit/commands/unpublish/workflow.py

import { WorkflowRepository } from '@n8n/db';
import { Command } from '@n8n/decorators';
import { Container } from '@n8n/di';
import { z } from 'zod';

import { BaseCommand } from '../base-command';

const flagsSchema = z.object({
	all: z.boolean().describe('Unpublish all workflows').optional(),
	id: z.string().describe('The ID of the workflow to unpublish').optional(),
});

@Command({
	name: 'unpublish:workflow',
	description: 'Unpublish workflow(s)',
	examples: ['--all', '--id=5'],
	flagsSchema,
})
export class UnpublishWorkflowCommand extends BaseCommand<z.infer<typeof flagsSchema>> {
	async run() {
		const { flags } = this;

		if (!flags.all && !flags.id) {
			this.logger.error('Either option "--all" or "--id" must be set.');
			return;
		}

		if (flags.all && flags.id) {
			this.logger.error('Cannot use both "--all" and "--id" flags together.');
			return;
		}

		if (flags.id) {
			this.logger.info(`Unpublishing workflow with ID: ${flags.id}`);
			await Container.get(WorkflowRepository).updateActiveState(flags.id, false);
			this.logger.info('Workflow unpublished successfully');
		} else {
			this.logger.info('Unpublishing all workflows');
			await Container.get(WorkflowRepository).unpublishAll();
			this.logger.info('All workflows unpublished successfully');
		}

		this.logger.info('Note: Changes will not take effect if n8n is running.');
		this.logger.info('Please restart n8n for changes to take effect if n8n is currently running.');
	}

	async catch(error: Error) {
		this.logger.error('Error unpublishing workflow(s). See log messages for details.');
		this.logger.error('\nGOT ERROR');
		this.logger.error('====================================');
		this.logger.error(error.message);
		this.logger.error(error.stack!);
	}
}
