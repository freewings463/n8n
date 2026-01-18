"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/workflow-name.prompt.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/prompts/chains 的工作流模块。导入/依赖:外部:@langchain/core/prompts；内部:无；本地:../builder。导出:workflowNamingPromptTemplate。关键函数/方法:prompt。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/workflow-name.prompt.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/prompts/chains/workflow_name_prompt.py

import { PromptTemplate } from '@langchain/core/prompts';

import { prompt } from '../builder';

/** Template for generating descriptive workflow names from user prompts */
export const workflowNamingPromptTemplate = PromptTemplate.fromTemplate(
	prompt()
		.section(
			'role',
			'Based on the initial user prompt, please generate a name for the workflow that captures its essence and purpose',
		)
		.section('initial_prompt', '{initialPrompt}')
		.section(
			'output_rules',
			'This name should be concise, descriptive, and suitable for a workflow that automates tasks related to the given prompt. The name should be in a format that is easy to read and understand. Do not include the word "workflow" in the name.',
		)
		.build(),
);
