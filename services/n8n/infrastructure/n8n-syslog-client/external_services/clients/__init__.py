"""
MIGRATION-META:
  source_path: packages/@n8n/syslog-client/src/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/syslog-client/src 的入口。导入/依赖:外部:无；内部:无；本地:无。导出:SyslogClient、createClient、Facility、Severity、Transport。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。注释目标:A syslog client for Node.js supporting UDP, TCP, TLS, and Unix socket transports. / Supports both RFC 3164 and RFC 5424 syslog message formats.。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/syslog-client treated as external service client library
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/syslog-client/src/index.ts -> services/n8n/infrastructure/n8n-syslog-client/external_services/clients/__init__.py

/**
 * @n8n/syslog-client
 *
 * A syslog client for Node.js supporting UDP, TCP, TLS, and Unix socket transports.
 * Supports both RFC 3164 and RFC 5424 syslog message formats.
 *
 * Based upon the great work done in:
 * https://github.com/paulgrove/node-syslog-client
 */

export { SyslogClient } from './client';
export { createClient } from './factory';
export { Facility, Severity, Transport } from './constants';
export type { ClientOptions, DateFormatter, LogOptions, SyslogCallback } from './types';
export {
	ConnectionError,
	SyslogClientError,
	TimeoutError,
	TransportError,
	ValidationError,
} from './errors';
