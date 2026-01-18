"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/prompts/builder/types.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/prompts/builder 的工作流类型。导入/依赖:外部:无；内部:无；本地:无。导出:SectionFormat、ContentOrFactory、SectionOptions、PromptBuilderOptions、SectionEntry、MessageBlock。关键函数/方法:无。用于定义工作流相关类型/结构约束，供多模块共享。注释目标:Format type for section output / - 'xml': Wraps content in XML-style tags <section_name>content</section_name>。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/prompts/builder/types.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/prompts/builder/types.py

/**
 * Format type for section output
 * - 'xml': Wraps content in XML-style tags <section_name>content</section_name>
 * - 'markdown': Uses markdown headers ## SECTION NAME
 */
export type SectionFormat = 'xml' | 'markdown';

/**
 * Content can be a string or a factory function for lazy evaluation.
 * Factory functions are only called during build() and can return null/undefined
 * to skip the section.
 */
export type ContentOrFactory = string | (() => string | null | undefined);

/**
 * Options for individual sections
 */
export interface SectionOptions {
	/**
	 * Custom tag/header name. Defaults to normalized section name.
	 * For XML: becomes the tag name
	 * For Markdown: becomes the header text
	 */
	tag?: string;

	/**
	 * Whether to add LangChain cache_control to this section.
	 * Only affects buildAsMessageBlocks() output.
	 * Default: false
	 */
	cache?: boolean;
}

/**
 * Options for the PromptBuilder constructor
 */
export interface PromptBuilderOptions {
	/**
	 * Output format for sections.
	 * Default: 'xml'
	 */
	format?: SectionFormat;

	/**
	 * Separator between sections.
	 * Default: '\n\n'
	 */
	separator?: string;
}

/**
 * Internal representation of a section
 */
export interface SectionEntry {
	/** Display name of the section */
	name: string;

	/** Content or factory function */
	content: ContentOrFactory;

	/** Section options */
	options: SectionOptions;
}

/**
 * LangChain message block format
 */
export interface MessageBlock {
	type: 'text';
	text: string;
	cache_control?: { type: 'ephemeral' };
}
