"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater/instance-url.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater 的工作流模块。导入/依赖:外部:无；内部:@/prompts/builder；本地:无。导出:instanceUrlPrompt。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater/instance-url.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/prompts/chains/parameter-updater/instance_url.py

import { PromptBuilder } from '@/prompts/builder';

export const instanceUrlPrompt = new PromptBuilder()
	.section(
		'instance_url',
		`The n8n instance base URL is: {instanceUrl}

This URL is essential for webhook nodes and chat triggers as it provides the base URL for:
- Webhook URLs that external services need to call
- Chat trigger URLs for conversational interfaces
- Any node that requires the full instance URL to generate proper callback URLs

When working with webhook or chat trigger nodes, use this URL as the base for constructing proper endpoint URLs.`,
	)
	.build();
