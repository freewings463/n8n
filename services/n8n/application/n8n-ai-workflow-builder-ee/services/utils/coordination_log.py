"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/utils/coordination-log.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/utils 的工作流工具。导入/依赖:外部:无；内部:无；本地:无。导出:RoutingDecision、getLastCompletedPhase、getPhaseEntry、hasPhaseCompleted 等8项。关键函数/方法:getLastCompletedPhase、getPhaseEntry、hasPhaseCompleted、getConfiguratorOutput 等7项。用于提供工作流通用工具能力（纯函数/封装器）供复用。注释目标:Coordination log utilities for deterministic routing between subgraphs. / These utilities parse the…。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/utils/coordination-log.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/utils/coordination_log.py

/**
 * Coordination log utilities for deterministic routing between subgraphs.
 *
 * These utilities parse the coordination log to determine:
 * 1. Which subgraphs have completed
 * 2. What the next routing decision should be
 * 3. What output data is available from each phase
 */

import type {
	CoordinationLogEntry,
	SubgraphPhase,
	DiscoveryMetadata,
	BuilderMetadata,
	ConfiguratorMetadata,
	StateManagementMetadata,
} from '../types/coordination';

export type RoutingDecision = 'discovery' | 'builder' | 'configurator' | 'responder';

/**
 * Get the last completed phase from the coordination log
 */
export function getLastCompletedPhase(log: CoordinationLogEntry[]): SubgraphPhase | null {
	if (log.length === 0) return null;

	// Find the most recent completed entry
	for (let i = log.length - 1; i >= 0; i--) {
		if (log[i].status === 'completed') {
			return log[i].phase;
		}
	}
	return null;
}

/**
 * Get entry for a specific phase
 */
export function getPhaseEntry(
	log: CoordinationLogEntry[],
	phase: SubgraphPhase,
): CoordinationLogEntry | null {
	return log.find((entry) => entry.phase === phase && entry.status === 'completed') ?? null;
}

/**
 * Check if a phase has completed
 */
export function hasPhaseCompleted(log: CoordinationLogEntry[], phase: SubgraphPhase): boolean {
	return log.some((entry) => entry.phase === phase && entry.status === 'completed');
}

/**
 * Get configurator output (setup instructions) from the log
 */
export function getConfiguratorOutput(log: CoordinationLogEntry[]): string | null {
	const entry = getPhaseEntry(log, 'configurator');
	return entry?.output ?? null;
}

/**
 * Get builder output (workflow summary) from the log
 */
export function getBuilderOutput(log: CoordinationLogEntry[]): string | null {
	const entry = getPhaseEntry(log, 'builder');
	return entry?.output ?? null;
}

/**
 * Get typed metadata for a specific phase
 */
export function getPhaseMetadata(
	log: CoordinationLogEntry[],
	phase: 'discovery',
): DiscoveryMetadata | null;
export function getPhaseMetadata(
	log: CoordinationLogEntry[],
	phase: 'builder',
): BuilderMetadata | null;
export function getPhaseMetadata(
	log: CoordinationLogEntry[],
	phase: 'configurator',
): ConfiguratorMetadata | null;
export function getPhaseMetadata(
	log: CoordinationLogEntry[],
	phase: 'state_management',
): StateManagementMetadata | null;
export function getPhaseMetadata(
	log: CoordinationLogEntry[],
	phase: SubgraphPhase,
): DiscoveryMetadata | BuilderMetadata | ConfiguratorMetadata | StateManagementMetadata | null {
	const entry = getPhaseEntry(log, phase);
	if (!entry) return null;

	// Error entries have phase: 'error' in metadata, completed entries have the subgraph phase
	if (entry.metadata.phase === 'error') return null;

	return entry.metadata;
}

/**
 * Check if any phase has an error status
 */
export function hasErrorInLog(log: CoordinationLogEntry[]): boolean {
	return log.some((entry) => entry.status === 'error');
}

/**
 * Get error entry from coordination log (if any)
 */
export function getErrorEntry(log: CoordinationLogEntry[]): CoordinationLogEntry | null {
	return log.find((entry) => entry.status === 'error') ?? null;
}

/**
 * Check if recursion errors have been cleared (AI-1812)
 * Returns true if there's a state_management entry that cleared recursion errors
 */
export function hasRecursionErrorsCleared(log: CoordinationLogEntry[]): boolean {
	return log.some(
		(entry) =>
			entry.phase === 'state_management' &&
			entry.summary.includes('Cleared') &&
			entry.summary.includes('recursion'),
	);
}

/**
 * Deterministic routing based on coordination log.
 * Called AFTER a subgraph completes to determine next phase.
 */
export function getNextPhaseFromLog(log: CoordinationLogEntry[]): RoutingDecision {
	// If any phase errored, route to responder to report the error
	// UNLESS recursion errors have been acknowledged/cleared (AI-1812)
	const hasErrors = hasErrorInLog(log);

	if (hasErrors) {
		// Check if recursion errors were cleared
		if (!hasRecursionErrorsCleared(log)) {
			// No clear marker - route to responder
			return 'responder';
		}

		// Find the last clear marker to check for errors after it
		const lastClearIndex = log.findLastIndex(
			(entry) =>
				entry.phase === 'state_management' &&
				entry.summary.includes('Cleared') &&
				entry.summary.includes('recursion'),
		);

		// Check if any errors exist after the clear marker
		const hasErrorsAfterClear = log
			.slice(lastClearIndex + 1)
			.some((entry) => entry.status === 'error');

		if (hasErrorsAfterClear) {
			return 'responder';
		}
	}

	const lastPhase = getLastCompletedPhase(log);
	// After discovery → always builder (builder decides what new nodes to add)
	if (lastPhase === 'discovery') {
		return 'builder';
	}

	// After builder → configurator
	if (lastPhase === 'builder') {
		return 'configurator';
	}

	// After configurator → responder (terminal)
	if (lastPhase === 'configurator') {
		return 'responder';
	}

	// No phases completed yet → let supervisor decide
	return 'responder';
}

/**
 * Build a summary of completed phases for debugging/logging
 */
export function summarizeCoordinationLog(log: CoordinationLogEntry[]): string {
	if (log.length === 0) return 'No phases completed';

	return log
		.filter((e) => e.status === 'completed')
		.map((e) => `${e.phase}: ${e.summary}`)
		.join(' → ');
}
