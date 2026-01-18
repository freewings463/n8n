"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/utils/timed-query.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/db/src/utils 的工具。导入/依赖:外部:无；内部:@n8n/backend-common、@n8n/decorators、@n8n/di；本地:无。导出:TimedQuery。关键函数/方法:无。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/utils/timed-query.ts -> services/n8n/application/n8n-db/services/utils/timed_query.py

import { Logger } from '@n8n/backend-common';
import { Timed } from '@n8n/decorators';
import { Container } from '@n8n/di';

/**
 * Decorator that warns when database queries exceed a duration threshold.
 *
 * For options, see `@n8n/decorators/src/timed.ts`.
 *
 * @example
 * ```ts
 * @Service()
 * class UserRepository {
 *   @TimedQuery()
 *   async findUsers() {
 *     // will log warning if execution takes > 100ms
 *   }
 *
 *   @TimedQuery({ threshold: 50, logArgs: true })
 *   async findUserById(id: string) {
 *     // will log warning if execution takes >50ms, including args
 *   }
 * }
 * ```
 */
export const TimedQuery = Timed(Container.get(Logger), 'Slow database query');
