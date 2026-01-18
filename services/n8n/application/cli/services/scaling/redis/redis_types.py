"""
MIGRATION-META:
  source_path: packages/cli/src/scaling/redis/redis.types.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/scaling/redis 的类型。导入/依赖:外部:无；内部:无；本地:无。导出:RedisClientType。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/scaling/redis/redis.types.ts -> services/n8n/application/cli/services/scaling/redis/redis_types.py

export type RedisClientType = N8nRedisClientType | BullRedisClientType;

/**
 * Redis client used by n8n.
 *
 * - `subscriber(n8n)` to listen for messages from scaling mode pubsub channels
 * - `publisher(n8n)` to send messages into scaling mode pubsub channels
 * - `cache(n8n)` for caching operations (variables, resource ownership, etc.)
 */
type N8nRedisClientType = 'subscriber(n8n)' | 'publisher(n8n)' | 'cache(n8n)';

/**
 * Redis client used internally by Bull. Suffixed with `(bull)` at `ScalingService.setupQueue`.
 *
 * - `subscriber(bull)` for event listening
 * - `client(bull)` for general queue operations
 * - `bclient(bull)` for blocking operations when processing jobs
 */
type BullRedisClientType = 'subscriber(bull)' | 'client(bull)' | 'bclient(bull)';
