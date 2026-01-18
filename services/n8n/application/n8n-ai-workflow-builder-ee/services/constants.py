"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/constants.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src 的工作流模块。导入/依赖:外部:无；内部:无；本地:无。导出:MAX_AI_BUILDER_PROMPT_LENGTH、MAX_TOTAL_TOKENS、MAX_OUTPUT_TOKENS、MAX_INPUT_TOKENS、MAX_PARAMETER_VALUE_LENGTH、DEFAULT_AUTO_COMPACT_THRESHOLD_TOKENS 等8项。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。注释目标:Maximum length of user prompt message in characters. / Prevents excessively long messages that could consume too many tokens.。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/constants.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/constants.py

/**
 * Maximum length of user prompt message in characters.
 * Prevents excessively long messages that could consume too many tokens.
 */
export const MAX_AI_BUILDER_PROMPT_LENGTH = 5000; // characters

/**
 * Token limits for the LLM context window.
 */
export const MAX_TOTAL_TOKENS = 200_000;
export const MAX_OUTPUT_TOKENS = 16_000;
export const MAX_INPUT_TOKENS = MAX_TOTAL_TOKENS - MAX_OUTPUT_TOKENS - 5_000;

/**
 * Maximum length of individual parameter value that can be retrieved via tool call.
 * Prevents tool responses from becoming too large and filling up the context.
 */
export const MAX_PARAMETER_VALUE_LENGTH = 30_000;

/**
 * Token threshold for automatically compacting conversation history.
 * When conversation exceeds this limit, older messages are summarized to free up space.
 * Set to 150k tokens to provide a safety margin before hitting the MAX_INPUT_TOKENS limit.
 * This includes all token types: input, output, cache_creation, and cache_read tokens.
 */
export const DEFAULT_AUTO_COMPACT_THRESHOLD_TOKENS = MAX_TOTAL_TOKENS - 50_000;

/**
 * Maximum token count for workflow JSON after trimming.
 * Used to determine when a workflow is small enough to include in context.
 */
export const MAX_WORKFLOW_LENGTH_TOKENS = 30_000;

/**
 * Average character-to-token ratio for Anthropic models.
 * Used for rough token count estimation from character counts.
 */
export const AVG_CHARS_PER_TOKEN_ANTHROPIC = 3.5;

/**
 * Maximum characters allowed for a single node example configuration.
 * Examples exceeding this limit are filtered out to avoid context bloat.
 * Based on ~5000 tokens at AVG_CHARS_PER_TOKEN_ANTHROPIC ratio.
 */
export const MAX_NODE_EXAMPLE_CHARS = 5000 * AVG_CHARS_PER_TOKEN_ANTHROPIC;

/**
 * Maximum iterations for subgraph tool loops.
 * Prevents infinite loops when agents keep calling tools without finishing.
 */
export const MAX_BUILDER_ITERATIONS = 30;
export const MAX_CONFIGURATOR_ITERATIONS = 30;
export const MAX_DISCOVERY_ITERATIONS = 50;
export const MAX_MULTI_AGENT_STREAM_ITERATIONS =
	MAX_BUILDER_ITERATIONS + MAX_CONFIGURATOR_ITERATIONS + MAX_DISCOVERY_ITERATIONS;
export const MAX_SINGLE_AGENT_STREAM_ITERATIONS = 50;
