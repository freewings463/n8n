"""
MIGRATION-META:
  source_path: packages/@n8n/config/src/configs/cache.config.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/config/src/configs 的配置。导入/依赖:外部:zod；内部:无；本地:../decorators。导出:CacheConfig。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/config treated as infrastructure configuration/runtime environment
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/config/src/configs/cache.config.ts -> services/n8n/infrastructure/n8n-config/configuration/configs/cache_config.py

import { z } from 'zod';

import { Config, Env, Nested } from '../decorators';

const cacheBackendSchema = z.enum(['memory', 'redis', 'auto']);
type CacheBackend = z.infer<typeof cacheBackendSchema>;

@Config
class MemoryConfig {
	/** Max size of memory cache in bytes */
	@Env('N8N_CACHE_MEMORY_MAX_SIZE')
	maxSize: number = 3 * 1024 * 1024; // 3 MiB

	/** Time to live (in milliseconds) for data cached in memory. */
	@Env('N8N_CACHE_MEMORY_TTL')
	ttl: number = 3600 * 1000; // 1 hour
}

@Config
class RedisConfig {
	/** Prefix for cache keys in Redis. */
	@Env('N8N_CACHE_REDIS_KEY_PREFIX')
	prefix: string = 'cache';

	/** Time to live (in milliseconds) for data cached in Redis. 0 for no TTL. */
	@Env('N8N_CACHE_REDIS_TTL')
	ttl: number = 3600 * 1000; // 1 hour
}

@Config
export class CacheConfig {
	/** Backend to use for caching. */
	@Env('N8N_CACHE_BACKEND', cacheBackendSchema)
	backend: CacheBackend = 'auto';

	@Nested
	memory: MemoryConfig;

	@Nested
	redis: RedisConfig;
}
