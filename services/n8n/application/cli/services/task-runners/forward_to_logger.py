"""
MIGRATION-META:
  source_path: packages/cli/src/task-runners/forward-to-logger.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/task-runners 的模块。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:forwardToLogger。关键函数/方法:forwardToLogger、stringify。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/task-runners/forward-to-logger.ts -> services/n8n/application/cli/services/task-runners/forward_to_logger.py

import type { Logger } from 'n8n-workflow';
import type { Readable } from 'stream';

/**
 * Forwards stdout and stderr of a given producer to the given
 * logger's info and error methods respectively.
 */
export function forwardToLogger(
	logger: Logger,
	producer: {
		stdout?: Readable | null;
		stderr?: Readable | null;
	},
	prefix?: string,
) {
	if (prefix) {
		prefix = prefix.trimEnd();
	}

	const stringify = (data: Buffer) => {
		let str = data.toString();

		// Remove possible trailing newline (otherwise it's duplicated)
		if (str.endsWith('\n')) {
			str = str.slice(0, -1);
		}

		return prefix ? `${prefix} ${str}` : str;
	};

	if (producer.stdout) {
		producer.stdout.on('data', (data: Buffer) => {
			logger.info(stringify(data));
		});
	}

	if (producer.stderr) {
		producer.stderr.on('data', (data: Buffer) => {
			logger.error(stringify(data));
		});
	}
}
