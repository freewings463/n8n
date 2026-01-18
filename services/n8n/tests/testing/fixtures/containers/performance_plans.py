"""
MIGRATION-META:
  source_path: packages/testing/containers/performance-plans.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/containers 的模块。导入/依赖:外部:无；内部:无；本地:无。导出:BasePerformancePlan、BASE_PERFORMANCE_PLANS、PerformancePlanName、isValidPerformancePlan。关键函数/方法:isValidPerformancePlan。用于承载该模块实现细节，并通过导出对外提供能力。注释目标:Shared Performance Plan Types and Configurations / This file provides the base performance plan definitions that can be used by:。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Testing package (containers harness) -> tests/fixtures/containers
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/containers/performance-plans.ts -> services/n8n/tests/testing/fixtures/containers/performance_plans.py

/**
 * Shared Performance Plan Types and Configurations
 *
 * This file provides the base performance plan definitions that can be used by:
 * - CLI tools (n8n-start-stack.ts)
 * - Playwright tests (cloud-only.ts)
 *
 */

// Base performance plan configuration (resource constraints only)
export interface BasePerformancePlan {
	memory: number; // in GB
	cpu: number; // in cores
}

export const BASE_PERFORMANCE_PLANS: Record<string, BasePerformancePlan> = {
	trial: { memory: 0.75, cpu: 1 }, // 768MB RAM, 1000 millicore CPU
	starter: { memory: 0.75, cpu: 1 }, // 768MB RAM, 1000 millicore CPU
	pro1: { memory: 1.25, cpu: 1 }, // 1.25GB RAM, 1000 millicore CPU
	pro2: { memory: 2.5, cpu: 1.5 }, // 2.5GB RAM, 1500 millicore CPU
	enterprise: { memory: 8.0, cpu: 2.0 }, // 8GB RAM, 2.0 CPU core
} as const;

export type PerformancePlanName = keyof typeof BASE_PERFORMANCE_PLANS;

export function isValidPerformancePlan(name: string): name is PerformancePlanName {
	return name in BASE_PERFORMANCE_PLANS;
}
