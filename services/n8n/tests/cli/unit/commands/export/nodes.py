"""
MIGRATION-META:
  source_path: packages/cli/src/commands/export/nodes.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/commands/export 的模块。导入/依赖:外部:fs/promises、zod；内部:@n8n/decorators、@n8n/di、n8n-workflow、@/load-nodes-and-credentials；本地:../base-command。导出:ExportNodes。关键函数/方法:run、writeNodesJSON。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/commands/export/nodes.ts -> services/n8n/tests/cli/unit/commands/export/nodes.py

import { Command } from '@n8n/decorators';
import { Container } from '@n8n/di';
import { createWriteStream } from 'fs';
import { mkdir } from 'fs/promises';
import type { INodeTypeBaseDescription } from 'n8n-workflow';
import path from 'path';
import z from 'zod';

import { LoadNodesAndCredentials } from '@/load-nodes-and-credentials';

import { BaseCommand } from '../base-command';

const flagsSchema = z.object({
	output: z
		.string()
		.default('./nodes.json')
		.describe('Path to the output file for node types JSON'),
});

@Command({
	name: 'export:nodes',
	description: 'Export all node types to a JSON file',
	examples: ['', '--output=/tmp/nodes.json'],
	flagsSchema,
})
export class ExportNodes extends BaseCommand<z.infer<typeof flagsSchema>> {
	async run() {
		const outputPath = path.resolve(this.flags.output);
		const outputDir = path.dirname(outputPath);

		this.logger.info(`Exporting node types to ${outputPath}...`);

		// Ensure output directory exists
		await mkdir(outputDir, { recursive: true });

		const loadNodesAndCredentials = Container.get(LoadNodesAndCredentials);
		const { nodes } = loadNodesAndCredentials.types;

		this.logger.info(`Found ${nodes.length} node types`);

		// Write nodes to JSON file using streaming
		this.writeNodesJSON(outputPath, nodes);

		this.logger.info(`Successfully exported ${nodes.length} node types to ${outputPath}`);
	}

	private writeNodesJSON(filePath: string, nodes: INodeTypeBaseDescription[]) {
		const stream = createWriteStream(filePath, 'utf-8');
		stream.write('[\n');
		nodes.forEach((entry, index) => {
			stream.write(JSON.stringify(entry));
			if (index !== nodes.length - 1) stream.write(',');
			stream.write('\n');
		});
		stream.write(']\n');
		stream.end();
	}
}
