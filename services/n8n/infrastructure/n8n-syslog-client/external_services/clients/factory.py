"""
MIGRATION-META:
  source_path: packages/@n8n/syslog-client/src/factory.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/syslog-client/src 的模块。导入/依赖:外部:无；内部:无；本地:./client、./types。导出:createClient。关键函数/方法:createClient。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/syslog-client treated as external service client library
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/syslog-client/src/factory.ts -> services/n8n/infrastructure/n8n-syslog-client/external_services/clients/factory.py

import { SyslogClient } from './client';
import type { ClientOptions } from './types';

/**
 * Factory function to create a syslog client.
 * Provided for backward compatibility with original API.
 *
 * @param target - Target host/path (IP address, hostname, or Unix socket path)
 * @param options - Client configuration options
 * @returns New SyslogClient instance
 *
 * @example
 * ```typescript
 * import { createClient, Transport } from '@n8n/syslog-client';
 *
 * const client = createClient('192.168.1.1', {
 *   transport: Transport.Tcp,
 *   port: 514,
 * });
 *
 * await client.log('Test message');
 * client.close();
 * ```
 */
export function createClient(target?: string, options?: ClientOptions): SyslogClient {
	return new SyslogClient(target, options);
}
