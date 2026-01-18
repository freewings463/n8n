"""
MIGRATION-META:
  source_path: packages/cli/src/services/cache/cache.types.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/services/cache 的服务。导入/依赖:外部:cache-manager；内部:@/services/…/redis.cache-manager；本地:无。导出:TaggedRedisCache、TaggedMemoryCache、Hash、MaybeHash。关键函数/方法:无。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/services/cache/cache.types.ts -> services/n8n/application/cli/services/services/cache/cache_types.py

import type { MemoryCache } from 'cache-manager';

import type { RedisCache } from '@/services/cache/redis.cache-manager';

export type TaggedRedisCache = RedisCache & { kind: 'redis' };

export type TaggedMemoryCache = MemoryCache & { kind: 'memory' };

export type Hash<T = unknown> = Record<string, T>;

export type MaybeHash<T> = Hash<T> | undefined;
