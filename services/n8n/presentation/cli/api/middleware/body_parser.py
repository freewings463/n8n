"""
MIGRATION-META:
  source_path: packages/cli/src/middlewares/body-parser.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/middlewares 的模块。导入/依赖:外部:express、querystring、raw-body、xml2js、zlib；内部:@n8n/config、@n8n/di、n8n-core、n8n-workflow、@/errors/…/unprocessable.error；本地:无。导出:rawBodyReader、parseBody、bodyParser。关键函数/方法:parseIncomingMessage、next、parseBody。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected Express RequestHandler-style middleware
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/middlewares/body-parser.ts -> services/n8n/presentation/cli/api/middleware/body_parser.py

import { GlobalConfig } from '@n8n/config';
import { Container } from '@n8n/di';
import type { Request, RequestHandler } from 'express';
import { parseIncomingMessage } from 'n8n-core';
import { jsonParse } from 'n8n-workflow';
import { parse as parseQueryString } from 'querystring';
import getRawBody from 'raw-body';
import { type Readable } from 'stream';
import { Parser as XmlParser } from 'xml2js';
import { createGunzip, createInflate } from 'zlib';

import { UnprocessableRequestError } from '@/errors/response-errors/unprocessable.error';

const xmlParser = new XmlParser({
	async: true,
	normalize: true, // Trim whitespace inside text nodes
	normalizeTags: true, // Transform tags to lowercase
	explicitArray: false, // Only put properties in array if length > 1
});

const payloadSizeMax = Container.get(GlobalConfig).endpoints.payloadSizeMax;
export const rawBodyReader: RequestHandler = async (req, _res, next) => {
	parseIncomingMessage(req);

	req.readRawBody = async () => {
		if (!req.rawBody) {
			let stream: Readable = req;
			let contentLength: string | undefined;
			const contentEncoding = req.headers['content-encoding'];
			switch (contentEncoding) {
				case 'gzip':
					stream = req.pipe(createGunzip());
					break;
				case 'deflate':
					stream = req.pipe(createInflate());
					break;
				default:
					contentLength = req.headers['content-length'];
			}
			req.rawBody = await getRawBody(stream, {
				length: contentLength,
				limit: `${String(payloadSizeMax)}mb`,
			});
			req._body = true;
		}
	};

	next();
};

export const parseBody = async (req: Request) => {
	// Skip multipart requests (e.g., file uploads) - these need specialized parsing by multer.
	// Reading the body stream here would consume it, making it unavailable for multer processing.
	if (req.contentType?.startsWith('multipart/')) {
		return;
	}

	await req.readRawBody();
	const { rawBody, contentType, encoding } = req;
	if (rawBody?.length) {
		try {
			if (contentType === 'application/json') {
				// eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
				req.body = jsonParse(rawBody.toString(encoding));
			} else if (contentType?.endsWith('/xml') || contentType?.endsWith('+xml')) {
				// eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
				req.body = await xmlParser.parseStringPromise(rawBody.toString(encoding));
			} else if (contentType === 'application/x-www-form-urlencoded') {
				req.body = parseQueryString(rawBody.toString(encoding), undefined, undefined, {
					maxKeys: 1000,
				});
			} else if (contentType === 'text/plain') {
				req.body = rawBody.toString(encoding);
			}
		} catch (error) {
			throw new UnprocessableRequestError('Failed to parse request body', (error as Error).message);
		}
	}
};

export const bodyParser: RequestHandler = async (req, _res, next) => {
	await parseBody(req);
	if (!req.body) req.body = {};
	next();
};
