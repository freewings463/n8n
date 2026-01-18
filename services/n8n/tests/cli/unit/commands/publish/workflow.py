"""
MIGRATION-META:
  source_path: packages/cli/src/commands/publish/workflow.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/commands/publish 的工作流模块。导入/依赖:外部:zod；内部:@n8n/db、@n8n/decorators、@n8n/di；本地:../base-command。导出:PublishWorkflowCommand。关键函数/方法:run。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/commands/publish/workflow.ts -> services/n8n/tests/cli/unit/commands/publish/workflow.py

import { WorkflowRepository } from '@n8n/db';
import { Command } from '@n8n/decorators';
import { Container } from '@n8n/di';
import { z } from 'zod';

import { BaseCommand } from '../base-command';

const flagsSchema = z.object({
	id: z.string().describe('The ID of the workflow to publish'),
	versionId: z
		.string()
		.describe('The version ID to publish. If not provided, publishes the current version')
		.optional(),
	all: z.boolean().describe('(Deprecated) This flag is no longer supported').optional(),
});

@Command({
	name: 'publish:workflow',
	description:
		'Publish a specific version of a workflow. If no version is specified, publishes the current version.',
	examples: ['--id=5 --versionId=abc123', '--id=5'],
	flagsSchema,
})
export class PublishWorkflowCommand extends BaseCommand<z.infer<typeof flagsSchema>> {
	async run() {
		const { flags } = this;

		// Educate users who try to use --all flag
		if (flags.all) {
			this.logger.error('The --all flag is no longer supported for workflow publishing.');
			this.logger.error(
				'Please publish workflows individually using: publish:workflow --id=<workflow-id> [--versionId=<version-id>]',
			);
			return;
		}

		if (flags.versionId) {
			this.logger.info(`Publishing workflow with ID: ${flags.id}, version: ${flags.versionId}`);
		} else {
			this.logger.info(`Publishing workflow with ID: ${flags.id} (current version)`);
		}

		await Container.get(WorkflowRepository).publishVersion(flags.id, flags.versionId);

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
