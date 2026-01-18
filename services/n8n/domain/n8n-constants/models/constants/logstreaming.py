"""
MIGRATION-META:
  source_path: packages/@n8n/constants/src/logstreaming.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/@n8n/constants/src 的模块。导入/依赖:外部:无；内部:无；本地:./time。导出:LOGSTREAMING_DEFAULT_MAX_FREE_SOCKETS、LOGSTREAMING_DEFAULT_MAX_SOCKETS、LOGSTREAMING_DEFAULT_MAX_TOTAL_SOCKETS、LOGSTREAMING_DEFAULT_SOCKET_TIMEOUT_MS、LOGSTREAMING_CB_DEFAULT_MAX_DURATION_MS、LOGSTREAMING_CB_DEFAULT_MAX_FAILURES、LOGSTREAMING_CB_DEFAULT_HALF_OPEN_REQUESTS 等2项。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/constants treated as domain constants
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/constants/src/logstreaming.ts -> services/n8n/domain/n8n-constants/models/constants/logstreaming.py

import { Time } from './time';

export const LOGSTREAMING_DEFAULT_MAX_FREE_SOCKETS = 5;
export const LOGSTREAMING_DEFAULT_MAX_SOCKETS = 50;
export const LOGSTREAMING_DEFAULT_MAX_TOTAL_SOCKETS = 100;
export const LOGSTREAMING_DEFAULT_SOCKET_TIMEOUT_MS = 5 * Time.seconds.toMilliseconds;

export const LOGSTREAMING_CB_DEFAULT_MAX_DURATION_MS = 3 * Time.minutes.toMilliseconds;
export const LOGSTREAMING_CB_DEFAULT_MAX_FAILURES = 5;
export const LOGSTREAMING_CB_DEFAULT_HALF_OPEN_REQUESTS = 2;
export const LOGSTREAMING_CB_DEFAULT_FAILURE_WINDOW_MS = 1 * Time.minutes.toMilliseconds;
export const LOGSTREAMING_CB_DEFAULT_CONCURRENT_HALF_OPEN_REQUESTS = 1;
