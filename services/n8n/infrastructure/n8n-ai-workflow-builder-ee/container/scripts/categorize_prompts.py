"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/scripts/categorize-prompts.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/scripts 的工作流模块。导入/依赖:外部:p-limit、picocolors；内部:无；本地:../chains/prompt-categorization、../integration/test-helpers、../types/categorization。导出:无。关键函数/方法:categorizeAllPrompts、processPrompt、elapsed、totalTime、isValidTechnique、writeFileSync。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected runtime IO/external interaction -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/scripts/categorize-prompts.ts -> services/n8n/infrastructure/n8n-ai-workflow-builder-ee/container/scripts/categorize_prompts.py

#!/usr/bin/env tsx

import { writeFileSync } from 'fs';
import pLimit from 'p-limit';
import { join } from 'path';
import pc from 'picocolors';

import { promptCategorizationChain } from '../src/chains/prompt-categorization';
import { setupIntegrationLLM } from '../src/chains/test/integration/test-helpers';
import { TechniqueDescription } from '../src/types/categorization';

// import { userPrompts } from '.prompts/100x3-prompts';

const userPrompts = [
	'Automate my business',
	'I want to build a workflow that generates a haiku from a wikipedia page.',
];

interface CategorizationResult {
	index: number;
	prompt: string;
	promptPreview: string;
	techniques: string[];
	confidence: number;
	executionTime: number;
}

async function categorizeAllPrompts() {
	// Get concurrency from environment or default to 10
	const DEFAULT_CONCURRENCY = 10;
	const parsedConcurrency = parseInt(process.env.CONCURRENCY ?? '', 10);
	const concurrency =
		!isNaN(parsedConcurrency) && parsedConcurrency >= 1 ? parsedConcurrency : DEFAULT_CONCURRENCY;

	console.log(pc.blue(`\n🚀 Starting categorization of ${userPrompts.length} prompts...`));
	console.log(pc.dim(`   Processing with concurrency=${concurrency}\n`));

	// Setup LLM
	const llm = await setupIntegrationLLM();

	const results: CategorizationResult[] = new Array(userPrompts.length).fill(
		null,
	) as CategorizationResult[];
	let completed = 0;
	const startTime = Date.now();

	// Create concurrency limiter
	const limit = pLimit(concurrency);

	// Process prompts in parallel with concurrency limit
	const processPrompt = async (prompt: string, i: number): Promise<void> => {
		const promptPreview = prompt.length > 80 ? prompt.substring(0, 80) + '...' : prompt;

		try {
			const taskStartTime = Date.now();
			const result = await promptCategorizationChain(llm, prompt);
			const executionTime = Date.now() - taskStartTime;

			results[i] = {
				index: i + 1,
				prompt,
				promptPreview,
				techniques: result.techniques,
				confidence: result.confidence ?? 0,
				executionTime,
			};

			completed++;
			const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
			console.log(
				pc.green(`✓ [${completed}/${userPrompts.length}]`) +
					pc.dim(` (${elapsed}s)`) +
					` ${promptPreview}\n  Techniques: ${result.techniques.join(', ')}\n  Confidence: ${((result.confidence ?? 0) * 100).toFixed(1)}%\n`,
			);
		} catch (error) {
			const errorMessage = error instanceof Error ? error.message : String(error);
			console.error(pc.red(`✗ [${i + 1}/${userPrompts.length}] Error:`) + ` ${errorMessage}\n`);
			results[i] = {
				index: i + 1,
				prompt,
				promptPreview,
				techniques: [],
				confidence: 0,
				executionTime: 0,
			};
			completed++;
		}
	};

	const promises = userPrompts.map(async (prompt, i) => {
		return await limit(async () => await processPrompt(prompt, i));
	});

	// Wait for all promises to complete
	await Promise.all(promises);
	const totalTime = ((Date.now() - startTime) / 1000).toFixed(1);

	// Calculate statistics
	const techniqueFrequency = new Map<string, number>();
	for (const result of results) {
		for (const technique of result.techniques) {
			techniqueFrequency.set(technique, (techniqueFrequency.get(technique) ?? 0) + 1);
		}
	}

	const sortedFrequency = Array.from(techniqueFrequency.entries()).sort((a, b) => b[1] - a[1]);

	const timestamp = new Date().toISOString().replace(/:/g, '-').split('.')[0];
	const outputDir = join(__dirname);

	// Type guard to check if a string is a valid technique key
	const isValidTechnique = (technique: string): technique is keyof typeof TechniqueDescription => {
		return technique in TechniqueDescription;
	};

	// Save technique frequency summary
	const summaryPath = join(outputDir, `categorization-summary-${timestamp}.md`);
	const summaryLines = [
		'# Prompt Categorization Summary',
		'',
		`**Date:** ${new Date().toISOString()}`,
		`**Total Prompts:** ${results.length}`,
		`**Total Time:** ${totalTime}s`,
		`**Concurrency:** ${concurrency} parallel executions`,
		`**Average Confidence:** ${((results.reduce((sum, r) => sum + r.confidence, 0) / results.length) * 100).toFixed(1)}%`,
		`**Average Execution Time:** ${(results.reduce((sum, r) => sum + r.executionTime, 0) / results.length).toFixed(0)}ms`,
		'',
		'## Technique Frequency',
		'',
		'| Rank | Technique | Used in | Description |',
		'|------|-----------|---------|-------------|',
		...sortedFrequency.map(([technique, count], index) => {
			const description = isValidTechnique(technique)
				? TechniqueDescription[technique]
				: 'Unknown technique';
			return `| ${index + 1} | \`${technique}\` | ${count} | ${description} |`;
		}),
		'',
		'## Detailed Results',
		'',
		...results.map((r) => {
			const preview =
				r.promptPreview.length > 100 ? r.promptPreview.substring(0, 100) + '...' : r.promptPreview;
			return [
				`### ${r.index}. ${preview}`,
				'',
				`**Techniques:** ${r.techniques.map((t) => `\`${t}\``).join(', ')}`,
				`**Confidence:** ${(r.confidence * 100).toFixed(1)}%`,
				`**Execution Time:** ${r.executionTime}ms`,
				'',
			].join('\n');
		}),
	];
	writeFileSync(summaryPath, summaryLines.join('\n'));

	console.log(pc.green('\n✓ Categorization complete!\n'));
	console.log(`Results saved to: ${pc.dim(summaryPath)}\n`);
}

// Run the script
categorizeAllPrompts().catch((error) => {
	console.error(pc.red('\n✗ Error:'), error);
	process.exit(1);
});
