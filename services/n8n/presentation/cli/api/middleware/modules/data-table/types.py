"""
MIGRATION-META:
  source_path: packages/cli/src/modules/data-table/types.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/modules/data-table 的类型。导入/依赖:外部:express；内部:@n8n/db；本地:无。导出:UploadMiddleware、MulterDestinationCallback、MulterFilenameCallback、AuthenticatedRequestWithFile、hasStringProperty。关键函数/方法:single。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected Express RequestHandler-style middleware
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/data-table/types.ts -> services/n8n/presentation/cli/api/middleware/modules/data-table/types.py

import type { AuthenticatedRequest } from '@n8n/db';
import type { RequestHandler } from 'express';

export interface UploadMiddleware {
	single(fieldName: string): RequestHandler;
}

export type MulterDestinationCallback = (error: Error | null, destination: string) => void;
export type MulterFilenameCallback = (error: Error | null, filename: string) => void;

export type AuthenticatedRequestWithFile<
	RouteParams = {},
	ResponseBody = {},
	RequestBody = {},
	RequestQuery = {},
> = AuthenticatedRequest<RouteParams, ResponseBody, RequestBody, RequestQuery> & {
	file?: Express.Multer.File;
	fileUploadError?: Error;
};

export function hasStringProperty<K extends string>(
	obj: unknown,
	key: K,
): obj is Record<K, string> & object {
	return typeof obj === 'object' && obj !== null && key in obj;
}
