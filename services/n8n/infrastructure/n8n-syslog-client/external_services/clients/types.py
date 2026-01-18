"""
MIGRATION-META:
  source_path: packages/@n8n/syslog-client/src/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/syslog-client/src 的类型。导入/依赖:外部:dgram、net、tls；内部:无；本地:./constants。导出:SyslogCallback、DateFormatter、ClientOptions、LogOptions、ResolvedLogOptions、TransportConnection。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/syslog-client treated as external service client library
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/syslog-client/src/types.ts -> services/n8n/infrastructure/n8n-syslog-client/external_services/clients/types.py

import type * as dgram from 'dgram';
import type * as net from 'net';
import type * as tls from 'tls';

import type { Facility, Severity, Transport } from './constants';

/**
 * Callback type for legacy API support.
 */
export type SyslogCallback = (error?: Error) => void;

/**
 * Date formatter function type.
 * Takes a Date object and returns a formatted string.
 */
export type DateFormatter = (date: Date) => string;

/**
 * Options for creating a syslog client.
 */
export interface ClientOptions {
	/**
	 * Hostname to use in syslog messages.
	 * @default os.hostname()
	 */
	syslogHostname?: string;

	/**
	 * Port number for TCP/TLS/UDP connections.
	 * @default 514
	 */
	port?: number;

	/**
	 * TCP connection timeout in milliseconds.
	 * @default 10000
	 */
	tcpTimeout?: number;

	/**
	 * Default facility for log messages.
	 * @default Facility.Local0
	 */
	facility?: Facility;

	/**
	 * Default severity for log messages.
	 * @default Severity.Informational
	 */
	severity?: Severity;

	/**
	 * Use RFC 3164 format (true) or RFC 5424 format (false).
	 * @default true
	 */
	rfc3164?: boolean;

	/**
	 * Application name for RFC 5424 format.
	 * @default process.title
	 */
	appName?: string;

	/**
	 * Custom date formatter function.
	 * @default Date.prototype.toISOString
	 */
	dateFormatter?: DateFormatter;

	/**
	 * UDP bind address for outgoing datagrams.
	 * If not specified, node will bind to 0.0.0.0.
	 */
	udpBindAddress?: string;

	/**
	 * Transport protocol to use.
	 * @default Transport.Udp
	 */
	transport?: Transport;

	/**
	 * TLS CA certificate(s). Only used when transport is Transport.Tls.
	 */
	tlsCA?: string | string[] | Buffer | Buffer[];
}

/**
 * Options for individual log messages.
 * These override the client defaults for a single message.
 */
export interface LogOptions {
	/**
	 * Override facility for this message.
	 */
	facility?: Facility;

	/**
	 * Override severity for this message.
	 */
	severity?: Severity;

	/**
	 * Override RFC format for this message.
	 */
	rfc3164?: boolean;

	/**
	 * Override app name for this message.
	 */
	appName?: string;

	/**
	 * Override syslog hostname for this message.
	 */
	syslogHostname?: string;

	/**
	 * Custom timestamp for the message.
	 * Useful for back-dating messages based on external timestamps.
	 */
	timestamp?: Date;

	/**
	 * Message ID for RFC 5424 format.
	 * @default "-"
	 */
	msgid?: string;
}

/**
 * Internal type for resolved log options with all defaults applied.
 */
export interface ResolvedLogOptions {
	facility: Facility;
	severity: Severity;
	rfc3164: boolean;
	appName: string;
	syslogHostname: string;
	timestamp?: Date;
	msgid?: string;
}

/**
 * Union type for all possible transport implementations.
 */
export type TransportConnection = dgram.Socket | net.Socket | tls.TLSSocket;
