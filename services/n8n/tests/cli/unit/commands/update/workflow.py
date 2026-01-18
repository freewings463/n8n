"""
MIGRATION-META:
  source_path: packages/cli/src/commands/update/workflow.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/commands/update 的工作流模块。导入/依赖:外部:zod；内部:@n8n/db、@n8n/decorators、@n8n/di；本地:../base-command。导出:UpdateWorkflowCommand。关键函数/方法:run。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/commands/update/workflow.ts -> services/n8n/tests/cli/unit/commands/update/workflow.py

import { WorkflowRepository } from '@n8n/db';
import { Command } from '@n8n/decorators';
import { Container } from '@n8n/di';
import { z } from 'zod';

import { BaseCommand } from '../base-command';

const flagsSchema = z.object({
	active: z.string().describe('Active state the workflow/s should be set to').optional(),
	all: z.boolean().describe('Operate on all workflows').optional(),
	id: z.string().describe('The ID of the workflow to operate on').optional(),
});

@Command({
	name: 'update:workflow',
	description: '[DEPRECATED] Update workflows - use publish:workflow or unpublish:workflow instead',
	examples: ['--all --active=false', '--id=5 --active=true'],
	flagsSchema,
})
export class UpdateWorkflowCommand extends BaseCommand<z.infer<typeof flagsSchema>> {
	async run() {
		const workflowRepository = Container.get(WorkflowRepository);
		const { flags } = this;

		this.logger.warn('⚠️  WARNING: The "update:workflow" command is deprecated.\n');

		if (!flags.all && !flags.id) {
			this.logger.error('Either option "--all" or "--id" have to be set!');
			return;
		}

		if (flags.all && flags.id) {
			this.logger.error(
				'Either something else on top should be "--all" or "--id" can be set never both!',
			);
			return;
		}

		if (flags.active === undefined) {
			this.logger.error('No update flag like "--active=true" has been set!');
			return;
		}

		if (!['false', 'true'].includes(flags.active)) {
			this.logger.error('Valid values for flag "--active" are only "false" or "true"!');
			return;
		}

		const newState = flags.active === 'true';
		const action = newState ? 'Activating' : 'Deactivating';

		// Backwards compatibility: if --id and --active=true, publish the current version
		if (flags.id && newState) {
			this.logger.info(`Publishing workflow ${flags.id} with current version`);
			this.logger.warn(`Please use: publish:workflow --id=${flags.id}\n`);
			try {
				await workflowRepository.publishVersion(flags.id);
			} catch (error) {
				this.logger.error('Failed to publish workflow');
				throw error;
			}

			this.logger.info('Note: Changes will not take effect if n8n is running.');
			this.logger.info(
				'Please restart n8n for changes to take effect if n8n is currently running.',
			);
			return;
		}

		// Block publishing with --all flag
		if (flags.all && newState) {
			this.logger.error('Workflow publishing via "update:workflow --all" is no longer supported.');
			this.logger.error(
				'Please publish workflows individually using: publish:workflow --id=<workflow-id>',
			);
			return;
		}

		// Show appropriate replacement command suggestion for unpublishing
		if (flags.id) {
			this.logger.warn(`Please use: unpublish:workflow --id=${flags.id}\n`);
		} else {
			this.logger.warn('Please use: unpublish:workflow --all\n');
		}

		if (flags.id) {
			this.logger.info(`${action} workflow with ID: ${flags.id}`);
			await workflowRepository.updateActiveState(flags.id, newState);
		} else {
			this.logger.info(`${action} all workflows`);
			await workflowRepository.unpublishAll();
		}

		this.logger.info('Note: Changes will not take effect if n8n is running.');
		this.logger.info('Please restart n8n for changes to take effect if n8n is currently running.');
	}

	async catch(error: Error) {
		this.logger.error('Error updating database. See log messages for details.');
		this.logger.error('\nGOT ERROR');
		this.logger.error('====================================');
		this.logger.error(error.message);
		this.logger.error(error.stack!);
	}
}
