"""
MIGRATION-META:
  source_path: packages/@n8n/decorators/src/controller/route.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/decorators/src/controller 的模块。导入/依赖:外部:express；内部:@n8n/di；本地:./controller-registry-metadata、./types。导出:Get、Post、Put、Patch、Delete、Head、Options。关键函数/方法:String。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected Express RequestHandler-style middleware
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/decorators/src/controller/route.ts -> services/n8n/presentation/n8n-decorators/api/middleware/controller/route.py

import { Container } from '@n8n/di';
import type { RequestHandler } from 'express';

import { ControllerRegistryMetadata } from './controller-registry-metadata';
import type { Controller, Method, RateLimit } from './types';

interface RouteOptions {
	middlewares?: RequestHandler[];
	usesTemplates?: boolean;
	/** When this flag is set to true, auth cookie isn't validated, and req.user will not be set */
	skipAuth?: boolean;
	allowSkipPreviewAuth?: boolean;
	/** When this flag is set to true, the auth cookie does not enforce MFA to be used in the token */
	allowSkipMFA?: boolean;
	/** When these options are set, calls to this endpoint are rate limited using the options */
	rateLimit?: boolean | RateLimit;
	/** When this flag is set to true, the endpoint is protected by API key */
	apiKeyAuth?: boolean;
}

const RouteFactory =
	(method: Method) =>
	(path: `/${string}`, options: RouteOptions = {}): MethodDecorator =>
	(target, handlerName) => {
		const routeMetadata = Container.get(ControllerRegistryMetadata).getRouteMetadata(
			target.constructor as Controller,
			String(handlerName),
		);
		routeMetadata.method = method;
		routeMetadata.path = path;
		routeMetadata.middlewares = options.middlewares ?? [];
		routeMetadata.usesTemplates = options.usesTemplates ?? false;
		routeMetadata.skipAuth = options.skipAuth ?? false;
		routeMetadata.allowSkipPreviewAuth = options.allowSkipPreviewAuth ?? false;
		routeMetadata.allowSkipMFA = options.allowSkipMFA ?? false;
		routeMetadata.apiKeyAuth = options.apiKeyAuth ?? false;
		routeMetadata.rateLimit = options.rateLimit;
	};

export const Get = RouteFactory('get');
export const Post = RouteFactory('post');
export const Put = RouteFactory('put');
export const Patch = RouteFactory('patch');
export const Delete = RouteFactory('delete');
export const Head = RouteFactory('head');
export const Options = RouteFactory('options');
