"""
MIGRATION-META:
  source_path: packages/cli/src/commands/export/entities.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/commands/export 的模块。导入/依赖:外部:zod；内部:@n8n/decorators、@n8n/di、@/services/export.service、@n8n/backend-common；本地:../base-command。导出:ExportEntitiesCommand。关键函数/方法:run。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/commands/export/entities.ts -> services/n8n/tests/cli/unit/commands/export/entities.py

import { Command } from '@n8n/decorators';
import { z } from 'zod';
import { Container } from '@n8n/di';

import { BaseCommand } from '../base-command';
import { ExportService } from '@/services/export.service';
import { safeJoinPath } from '@n8n/backend-common';

const flagsSchema = z.object({
	outputDir: z
		.string()
		.describe('Output directory path')
		.default(safeJoinPath(__dirname, './outputs')),
	includeExecutionHistoryDataTables: z.coerce
		.boolean()
		.describe(
			'Include execution history data tables, these are excluded by default as they can be very large',
		)
		.default(false),
	keyFile: z
		.string()
		.describe('Optional path to a file containing a custom encryption key')
		.optional(),
});

@Command({
	name: 'export:entities',
	description: 'Export database entities to JSON files',
	examples: [
		'',
		'--outputDir=./exports',
		'--outputDir=/path/to/backup',
		'--includeExecutionHistoryDataTables=true',
		'--keyFile=/path/to/key.txt',
		'--outputDir=./exports --keyFile=/path/to/key.txt',
	],
	flagsSchema,
})
export class ExportEntitiesCommand extends BaseCommand<z.infer<typeof flagsSchema>> {
	async run() {
		const outputDir = this.flags.outputDir;
		const excludedDataTables = new Set<string>();
		const keyFilePath = this.flags.keyFile ? safeJoinPath(this.flags.keyFile) : undefined;

		if (!this.flags.includeExecutionHistoryDataTables) {
			excludedDataTables.add('execution_annotation_tags');
			excludedDataTables.add('execution_annotations');
			excludedDataTables.add('execution_data');
			excludedDataTables.add('execution_entity');
			excludedDataTables.add('execution_metadata');
		}

		await Container.get(ExportService).exportEntities(outputDir, excludedDataTables, keyFilePath);
	}

	catch(error: Error) {
		this.logger.error('❌ Error exporting entities. See log messages for details. \n');
		this.logger.error('Error details:');
		this.logger.error('\n====================================\n');
		this.logger.error(`${error.message} \n`);
	}
}
