"""
MIGRATION-META:
  source_path: packages/workflow/src/logger-proxy.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src 的工作流模块。导入/依赖:外部:无；内部:无；本地:./interfaces。导出:error、warn、info、debug、init。关键函数/方法:init、noOp。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package workflow treated as domain model & rules
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/logger-proxy.ts -> services/n8n/domain/workflow/services/logger_proxy.py

import type { Logger } from './interfaces';

const noOp = () => {};
export let error: Logger['error'] = noOp;
export let warn: Logger['warn'] = noOp;
export let info: Logger['info'] = noOp;
export let debug: Logger['debug'] = noOp;

export const init = (logger: Logger) => {
	error = (message, meta) => logger.error(message, meta);
	warn = (message, meta) => logger.warn(message, meta);
	info = (message, meta) => logger.info(message, meta);
	debug = (message, meta) => logger.debug(message, meta);
};
