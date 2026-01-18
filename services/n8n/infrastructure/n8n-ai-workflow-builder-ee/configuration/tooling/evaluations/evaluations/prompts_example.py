"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/evaluations/prompts-example.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/evaluations 的工作流模块。导入/依赖:外部:无；内部:无；本地:无。导出:examplePrompts。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。注释目标:Example prompts for categorization evaluation / Use this format to create custom prompt sets for evaluation.。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI builder evaluation harness/scripts -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/evaluations/prompts-example.ts -> services/n8n/infrastructure/n8n-ai-workflow-builder-ee/configuration/tooling/evaluations/evaluations/prompts_example.py

/**
 * Example prompts for categorization evaluation
 *
 * Use this format to create custom prompt sets for evaluation.
 * You can export prompts from JSONL files using scripts/extract-user-prompts.js
 * and use them directly.
 *
 * To run with custom prompts:
 * 1. Create a file with an array of prompt strings
 * 2. Import and pass to runCategorizationEvaluation()
 */
export const examplePrompts = [
	'Create a workflow that monitors my website every 5 minutes and sends me a Slack notification if it goes down',
	'Build a chatbot that can answer customer questions about our product catalog using information from our knowledge base',
	'Set up a form to collect user feedback, analyze sentiment with AI, and store the results in Airtable',
	'Extract data from PDF invoices uploaded via form and update our accounting spreadsheet',
	'Scrape competitor pricing daily and generate a weekly summary report with price changes',
];

/**
 * Example usage:
 *
 * import { runCategorizationEvaluation } from './categorize-prompt-evaluation';
 * import { examplePrompts } from './prompts-example';
 *
 * runCategorizationEvaluation(examplePrompts).catch(console.error);
 */
