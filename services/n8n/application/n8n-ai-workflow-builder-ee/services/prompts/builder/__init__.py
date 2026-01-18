"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/prompts/builder/index.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/prompts/builder 的工作流入口。导入/依赖:外部:无；内部:无；本地:无。导出:PromptBuilder、prompt。关键函数/方法:无。用于汇总导出并完成工作流模块初始化、注册或装配。注释目标:PromptBuilder - A type-safe, fluent builder for composing LLM prompts. / ```typescript。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/prompts/builder/index.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/prompts/builder/__init__.py

/**
 * PromptBuilder - A type-safe, fluent builder for composing LLM prompts.
 *
 * @example
 * ```typescript
 * import { prompt } from '@/prompts/builder';
 *
 * const systemPrompt = prompt()
 *   .section('ROLE', 'You are an assistant')
 *   .sectionIf(hasContext, 'CONTEXT', () => buildContext())
 *   .examples('EXAMPLES', data, (ex) => `${ex.input} → ${ex.output}`)
 *   .build();
 * ```
 */

export { PromptBuilder, prompt } from './prompt-builder';

export type {
	ContentOrFactory,
	MessageBlock,
	PromptBuilderOptions,
	SectionFormat,
	SectionOptions,
} from './types';
