"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/utils/transformers.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/utils 的工具。导入/依赖:外部:无；内部:@n8n/config、@n8n/di、@n8n/typeorm、n8n-workflow；本地:无。导出:idStringifier、lowerCaser、objectRetriever、sqlite。关键函数/方法:无。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package @n8n/db defaulted to persistence infrastructure
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/utils/transformers.ts -> services/n8n/infrastructure/n8n-db/persistence/utils/transformers.py

import { GlobalConfig } from '@n8n/config';
import { Container } from '@n8n/di';
import type { ValueTransformer, FindOperator } from '@n8n/typeorm';
import { jsonParse } from 'n8n-workflow';

export const idStringifier = {
	from: (value?: number): string | undefined => value?.toString(),
	to: (
		value: string | FindOperator<unknown> | undefined,
	): number | FindOperator<unknown> | undefined =>
		typeof value === 'string' ? Number(value) : value,
};

export const lowerCaser = {
	from: (value: string): string => value,
	to: (value: string): string => (typeof value === 'string' ? value.toLowerCase() : value),
};

/**
 * Unmarshal JSON as JS object.
 */
export const objectRetriever: ValueTransformer = {
	to: (value: object): object => value,
	from: (value: string | object): object => (typeof value === 'string' ? jsonParse(value) : value),
};

/**
 * Transformer for sqlite JSON columns to mimic JSON-as-object behavior
 * from Postgres and MySQL.
 */
const jsonColumn: ValueTransformer = {
	to: (value: object): string | object =>
		Container.get(GlobalConfig).database.type === 'sqlite' ? JSON.stringify(value) : value,
	from: (value: string | object): object => (typeof value === 'string' ? jsonParse(value) : value),
};

export const sqlite = { jsonColumn };
