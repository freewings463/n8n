"""
MIGRATION-META:
  source_path: packages/@n8n/syslog-client/src/schemas.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/syslog-client/src 的模块。导入/依赖:外部:zod；内部:无；本地:./constants。导出:clientOptionsSchema、logOptionsSchema、ValidatedClientOptions、ValidatedLogOptions。关键函数/方法:createEnumSchema。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/syslog-client treated as external service client library
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/syslog-client/src/schemas.ts -> services/n8n/infrastructure/n8n-syslog-client/external_services/clients/schemas.py

import { z } from 'zod';

import { Facility, Severity, Transport } from './constants';

/**
 * Helper to dynamically create Zod schema for enum values.
 * Filters out string keys that regular enums create at runtime.
 */
const createEnumSchema = (enumObject: object, name: string) => {
	const values = Object.values(enumObject).filter((val) => typeof val === 'number');
	return z.number().refine((val) => values.includes(val), {
		message: `Invalid ${name} value. Must be one of: ${values.join(', ')}`,
	});
};

/**
 * Zod schema for validating ClientOptions.
 */
export const clientOptionsSchema = z.object({
	syslogHostname: z.string().optional(),
	port: z.number().int().positive().max(65535).optional(),
	tcpTimeout: z.number().int().positive().optional(),
	facility: createEnumSchema(Facility, 'facility').optional(),
	severity: createEnumSchema(Severity, 'severity').optional(),
	rfc3164: z.boolean().optional(),
	appName: z.string().max(48).optional(), // RFC 5424 limit
	dateFormatter: z.function().args(z.date()).returns(z.string()).optional(),
	udpBindAddress: z.string().ip().optional(),
	transport: createEnumSchema(Transport, 'transport').optional(),
	tlsCA: z
		.union([z.string(), z.array(z.string()), z.instanceof(Buffer), z.array(z.instanceof(Buffer))])
		.optional(),
});

/**
 * Zod schema for validating LogOptions.
 */
export const logOptionsSchema = z.object({
	facility: createEnumSchema(Facility, 'facility').optional(),
	severity: createEnumSchema(Severity, 'severity').optional(),
	rfc3164: z.boolean().optional(),
	appName: z.string().max(48).optional(),
	syslogHostname: z.string().optional(),
	timestamp: z.instanceof(Date).optional(),
	msgid: z.string().optional(),
});

/**
 * Inferred type from clientOptionsSchema for consistency.
 */
export type ValidatedClientOptions = z.infer<typeof clientOptionsSchema>;

/**
 * Inferred type from logOptionsSchema for consistency.
 */
export type ValidatedLogOptions = z.infer<typeof logOptionsSchema>;
