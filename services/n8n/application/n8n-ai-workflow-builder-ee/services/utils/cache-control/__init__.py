"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/utils/cache-control/index.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/utils/cache-control 的工作流入口。导入/依赖:外部:无；内部:无；本地:无。导出:无。关键函数/方法:无。用于汇总导出并完成工作流模块初始化、注册或装配。注释目标:Cache control utilities for optimizing Anthropic prompt caching. / This module implements a 4-breakpoint caching strategy that achieves 80-85% cache hit rates。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/utils/cache-control/index.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/utils/cache-control/__init__.py

/**
 * Cache control utilities for optimizing Anthropic prompt caching.
 *
 * This module implements a 4-breakpoint caching strategy that achieves 80-85% cache hit rates
 * by strategically placing cache markers and managing workflow context.
 *
 * @see README.md for detailed visualization and explanation
 */

export {
	findUserToolMessageIndices,
	cleanStaleWorkflowContext,
	applyCacheControlMarkers,
	applySubgraphCacheMarkers,
} from './helpers';
