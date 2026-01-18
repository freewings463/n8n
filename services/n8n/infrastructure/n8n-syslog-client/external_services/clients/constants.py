"""
MIGRATION-META:
  source_path: packages/@n8n/syslog-client/src/constants.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/syslog-client/src 的模块。导入/依赖:外部:无；内部:无；本地:无。导出:Transport、Facility、Severity。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。注释目标:eslint-disable no-restricted-syntax。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/syslog-client treated as external service client library
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/syslog-client/src/constants.ts -> services/n8n/infrastructure/n8n-syslog-client/external_services/clients/constants.py

/* eslint-disable no-restricted-syntax */
/* We want the runtime overhead here */

/**
 * Transport protocols supported by the syslog client.
 */
export enum Transport {
	Tcp = 1,
	Udp = 2,
	Tls = 3,
	Unix = 4,
}

/**
 * Syslog facility codes as defined in RFC 5424.
 */
export enum Facility {
	Kernel = 0,
	User = 1,
	Mail = 2,
	System = 3,
	// eslint-disable-next-line @typescript-eslint/no-duplicate-enum-values
	Daemon = 3,
	Auth = 4,
	Syslog = 5,
	Lpr = 6,
	News = 7,
	Uucp = 8,
	Cron = 9,
	Authpriv = 10,
	Ftp = 11,
	Audit = 13,
	Alert = 14,
	Local0 = 16,
	Local1 = 17,
	Local2 = 18,
	Local3 = 19,
	Local4 = 20,
	Local5 = 21,
	Local6 = 22,
	Local7 = 23,
}

/**
 * Syslog severity levels as defined in RFC 5424.
 */
export enum Severity {
	Emergency = 0,
	Alert = 1,
	Critical = 2,
	Error = 3,
	Warning = 4,
	Notice = 5,
	Informational = 6,
	Debug = 7,
}
