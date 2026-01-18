"""
MIGRATION-META:
  source_path: packages/@n8n/decorators/src/controller/types.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/decorators/src/controller 的类型。导入/依赖:外部:express；内部:@n8n/constants、@n8n/di、@n8n/permissions；本地:无。导出:Method、Arg、RateLimit、HandlerName、AccessScope、RouteMetadata、StaticRouterMetadata、ControllerMetadata 等1项。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected Express RequestHandler-style middleware
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/decorators/src/controller/types.ts -> services/n8n/presentation/n8n-decorators/api/middleware/controller/types.py

import type { BooleanLicenseFeature } from '@n8n/constants';
import type { Constructable } from '@n8n/di';
import type { Scope } from '@n8n/permissions';
import type { RequestHandler, Router } from 'express';

export type Method = 'get' | 'post' | 'put' | 'patch' | 'delete' | 'head' | 'options';

export type Arg = { type: 'body' | 'query' } | { type: 'param'; key: string };

export interface RateLimit {
	/**
	 * The maximum number of requests to allow during the `window` before rate limiting the client.
	 * @default 5
	 */
	limit?: number;
	/**
	 * How long we should remember the requests.
	 * @default 300_000 (5 minutes)
	 */
	windowMs?: number;
}

export type HandlerName = string;

export interface AccessScope {
	scope: Scope;
	globalOnly: boolean;
}

export interface RouteMetadata {
	method: Method;
	path: string;
	middlewares: RequestHandler[];
	usesTemplates: boolean;
	skipAuth: boolean;
	allowSkipPreviewAuth: boolean;
	allowSkipMFA: boolean;
	apiKeyAuth: boolean;
	rateLimit?: boolean | RateLimit;
	licenseFeature?: BooleanLicenseFeature;
	accessScope?: AccessScope;
	args: Arg[];
	router?: Router;
}

/**
 * Metadata for static routers mounted on a controller.
 * Picks relevant fields from RouteMetadata and makes router required.
 */
export type StaticRouterMetadata = {
	path: string;
	router: Router;
} & Partial<
	Pick<
		RouteMetadata,
		| 'skipAuth'
		| 'allowSkipPreviewAuth'
		| 'allowSkipMFA'
		| 'middlewares'
		| 'rateLimit'
		| 'licenseFeature'
		| 'accessScope'
	>
>;

export interface ControllerMetadata {
	basePath: `/${string}`;
	// If true, the controller will be registered on the root path without the any prefix
	registerOnRootPath?: boolean;
	middlewares: HandlerName[];
	routes: Map<HandlerName, RouteMetadata>;
}

export type Controller = Constructable<object> &
	Record<HandlerName, (...args: unknown[]) => Promise<unknown>>;
