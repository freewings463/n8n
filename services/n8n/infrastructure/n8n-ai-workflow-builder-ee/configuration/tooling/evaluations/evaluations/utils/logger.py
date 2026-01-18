"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/evaluations/utils/logger.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/evaluations/utils 的工作流工具。导入/依赖:外部:picocolors；内部:无；本地:无。导出:EvalLogger、createLogger。关键函数/方法:createLogger。用于提供工作流通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI builder evaluation harness/scripts -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/evaluations/utils/logger.ts -> services/n8n/infrastructure/n8n-ai-workflow-builder-ee/configuration/tooling/evaluations/evaluations/utils/logger.py

import pc from 'picocolors';

/**
 * Simple evaluation logger with verbose mode support.
 *
 * Usage:
 *   const log = createLogger(isVerbose);
 *   log.info('Always shown');
 *   log.verbose('Only shown in verbose mode');
 */

export interface EvalLogger {
	/** Always shown - important info */
	info: (message: string) => void;
	/** Only shown in verbose mode - debug details */
	verbose: (message: string) => void;
	/** Success messages (green) */
	success: (message: string) => void;
	/** Warning messages (yellow) */
	warn: (message: string) => void;
	/** Error messages (red) */
	error: (message: string) => void;
	/** Dimmed text for secondary info */
	dim: (message: string) => void;
	/** Check if verbose mode is enabled */
	isVerbose: boolean;
}

export function createLogger(verbose: boolean = false): EvalLogger {
	return {
		isVerbose: verbose,
		info: (message: string) => console.log(pc.blue(message)),
		verbose: (message: string) => {
			if (verbose) console.log(pc.dim(message));
		},
		success: (message: string) => console.log(pc.green(message)),
		warn: (message: string) => console.log(pc.yellow(message)),
		error: (message: string) => console.log(pc.red(message)),
		dim: (message: string) => console.log(pc.dim(message)),
	};
}
