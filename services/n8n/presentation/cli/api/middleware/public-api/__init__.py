"""
MIGRATION-META:
  source_path: packages/cli/src/public-api/index.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/public-api 的入口。导入/依赖:外部:express、express-openapi-validator/…/types、fs/promises、swagger-ui-express、validator、yamljs 等1项；内部:@n8n/config、@n8n/di、@/license、@/services/public-api-key.service、@/services/url.service；本地:无。导出:loadPublicApiVersions、isApiEnabled。关键函数/方法:setup、createApiRouter、serveFiles、openApiValidatorMiddleware、loadPublicApiVersions、isApiEnabled。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected Express RequestHandler-style middleware
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/public-api/index.ts -> services/n8n/presentation/cli/api/middleware/public-api/__init__.py

import { GlobalConfig } from '@n8n/config';
import { Container } from '@n8n/di';
import type { Router } from 'express';
import express from 'express';
import type { HttpError } from 'express-openapi-validator/dist/framework/types';
import fs from 'fs/promises';
import path from 'path';
import type { JsonObject } from 'swagger-ui-express';
import validator from 'validator';
import YAML from 'yamljs';

import { License } from '@/license';
import { PublicApiKeyService } from '@/services/public-api-key.service';
import { UrlService } from '@/services/url.service';

async function createApiRouter(
	version: string,
	openApiSpecPath: string,
	handlersDirectory: string,
	publicApiEndpoint: string,
): Promise<Router> {
	const n8nPath = Container.get(GlobalConfig).path;
	const swaggerDocument = YAML.load(openApiSpecPath) as JsonObject;
	// add the server depending on the config so the user can interact with the API
	// from the Swagger UI
	swaggerDocument.server = [
		{
			url: `${Container.get(UrlService).getInstanceBaseUrl()}/${publicApiEndpoint}/${version}}`,
		},
	];
	const apiController = express.Router();

	if (!Container.get(GlobalConfig).publicApi.swaggerUiDisabled) {
		const { serveFiles, setup } = await import('swagger-ui-express');
		const swaggerThemePath = path.join(__dirname, 'swagger-theme.css');
		const swaggerThemeCss = await fs.readFile(swaggerThemePath, { encoding: 'utf-8' });

		apiController.use(
			`/${publicApiEndpoint}/${version}/docs`,
			serveFiles(swaggerDocument),
			setup(swaggerDocument, {
				customCss: swaggerThemeCss,
				customSiteTitle: 'n8n Public API UI',
				customfavIcon: `${n8nPath}favicon.ico`,
			}),
		);
	}

	apiController.get(`/${publicApiEndpoint}/${version}/openapi.yml`, (_, res) => {
		res.sendFile(openApiSpecPath);
	});

	const { middleware: openApiValidatorMiddleware } = await import('express-openapi-validator');
	apiController.use(
		`/${publicApiEndpoint}/${version}`,
		express.json(),
		openApiValidatorMiddleware({
			apiSpec: openApiSpecPath,
			operationHandlers: handlersDirectory,
			validateRequests: true,
			validateApiSpec: true,
			formats: {
				email: {
					type: 'string',
					validate: (email: string) => validator.isEmail(email),
				},
				identifier: {
					type: 'string',
					validate: (identifier: string) =>
						validator.isUUID(identifier) || validator.isEmail(identifier),
				},
				jsonString: {
					validate: (data: string) => {
						try {
							JSON.parse(data);
							return true;
						} catch (e) {
							return false;
						}
					},
				},
			},
			validateSecurity: {
				handlers: {
					ApiKeyAuth: Container.get(PublicApiKeyService).getAuthMiddleware(version),
				},
			},
		}),
	);

	apiController.use(
		(
			error: HttpError,
			_req: express.Request,
			res: express.Response,
			_next: express.NextFunction,
		) => {
			res.status(error.status || 400).json({
				message: error.message,
			});
		},
	);

	return apiController;
}

export const loadPublicApiVersions = async (
	publicApiEndpoint: string,
): Promise<{ apiRouters: express.Router[]; apiLatestVersion: number }> => {
	const folders = await fs.readdir(__dirname);
	const versions = folders.filter((folderName) => folderName.startsWith('v'));

	const apiRouters = await Promise.all(
		versions.map(async (version) => {
			const openApiPath = path.join(__dirname, version, 'openapi.yml');
			return await createApiRouter(version, openApiPath, __dirname, publicApiEndpoint);
		}),
	);

	const version = versions.pop()?.charAt(1);

	return {
		apiRouters,
		apiLatestVersion: version ? Number(version) : 1,
	};
};

export function isApiEnabled(): boolean {
	return !Container.get(GlobalConfig).publicApi.disabled && !Container.get(License).isAPIDisabled();
}
