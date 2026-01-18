"""
MIGRATION-META:
  source_path: packages/cli/src/public-api/v1/shared/services/pagination.service.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/public-api/v1/shared 的服务。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:decodeCursor、encodeNextCursor。关键函数/方法:decodeCursor、encodeOffSetPagination、encodeCursorPagination、encodeNextCursor。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Public API adapter -> presentation/api/*
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/public-api/v1/shared/services/pagination.service.ts -> services/n8n/presentation/cli/api/v1/shared/services/pagination_service.py

import { jsonParse } from 'n8n-workflow';

import type {
	CursorPagination,
	OffsetPagination,
	PaginationCursorDecoded,
	PaginationOffsetDecoded,
} from '../../../types';

export const decodeCursor = (cursor: string): PaginationOffsetDecoded | PaginationCursorDecoded => {
	return jsonParse(Buffer.from(cursor, 'base64').toString());
};

const encodeOffSetPagination = (pagination: OffsetPagination): string | null => {
	if (pagination.numberOfTotalRecords > pagination.offset + pagination.limit) {
		return Buffer.from(
			JSON.stringify({
				limit: pagination.limit,
				offset: pagination.offset + pagination.limit,
			}),
		).toString('base64');
	}
	return null;
};

const encodeCursorPagination = (pagination: CursorPagination): string | null => {
	if (pagination.numberOfNextRecords) {
		return Buffer.from(
			JSON.stringify({
				lastId: pagination.lastId,
				limit: pagination.limit,
			}),
		).toString('base64');
	}
	return null;
};

export const encodeNextCursor = (
	pagination: OffsetPagination | CursorPagination,
): string | null => {
	if ('offset' in pagination) {
		return encodeOffSetPagination(pagination);
	}
	return encodeCursorPagination(pagination);
};
