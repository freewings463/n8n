"""
MIGRATION-META:
  source_path: packages/cli/src/response-helper.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src 的模块。导入/依赖:外部:express、picocolors；内部:@n8n/backend-common、@n8n/di、n8n-core、n8n-workflow；本地:../abstract/response.error。导出:sendSuccessResponse、sendErrorResponse、isUniqueConstraintError、reportError、send。关键函数/方法:sendSuccessResponse、isResponseError、sendErrorResponse、isUniqueConstraintError、reportError。用于承载该模块实现细节，并通过导出对外提供能力。注释目标:eslint-disable @typescript-eslint/no-unsafe-assignment。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/response-helper.ts -> services/n8n/presentation/cli/api/response_helper.py

/* eslint-disable @typescript-eslint/no-unsafe-assignment */
import { inDevelopment, Logger } from '@n8n/backend-common';
import { Container } from '@n8n/di';
import type { Request, Response } from 'express';
import { ErrorReporter } from 'n8n-core';
import { FORM_TRIGGER_PATH_IDENTIFIER, NodeApiError } from 'n8n-workflow';
import { Readable } from 'node:stream';
import picocolors from 'picocolors';

import { ResponseError } from './errors/response-errors/abstract/response.error';

export function sendSuccessResponse(
	res: Response,
	data: any,
	raw?: boolean,
	responseCode?: number,
	responseHeader?: object,
) {
	if (responseCode !== undefined) {
		res.status(responseCode);
	}

	if (responseHeader) {
		res.header(responseHeader);
	}

	if (data instanceof Readable) {
		data.pipe(res);
		return;
	}

	if (raw === true) {
		if (typeof data === 'string') {
			res.send(data);
		} else {
			res.json(data);
		}
	} else {
		res.json({
			data,
		});
	}
}

/**
 * Checks if the given error is a ResponseError. It can be either an
 * instance of ResponseError or an error which has the same properties.
 * The latter case is for external hooks.
 */
function isResponseError(error: Error): error is ResponseError {
	if (error instanceof ResponseError) {
		return true;
	}

	if (error instanceof Error) {
		return (
			'httpStatusCode' in error &&
			typeof error.httpStatusCode === 'number' &&
			'errorCode' in error &&
			typeof error.errorCode === 'number'
		);
	}

	return false;
}

interface ErrorResponse {
	code: number;
	message: string;
	hint?: string;
	stacktrace?: string;
	meta?: Record<string, unknown>;
}

export function sendErrorResponse(res: Response, error: Error) {
	let httpStatusCode = 500;

	const response: ErrorResponse = {
		code: 0,
		message: error.message ?? 'Unknown error',
	};

	if (isResponseError(error)) {
		if (inDevelopment) {
			Container.get(Logger).error(picocolors.red([error.httpStatusCode, error.message].join(' ')));
		}

		//render custom 404 page for form triggers
		const { originalUrl } = res.req;
		if (error.errorCode === 404 && originalUrl) {
			const basePath = originalUrl.split('/')[1];
			const isLegacyFormTrigger = originalUrl.includes(FORM_TRIGGER_PATH_IDENTIFIER);
			const isFormTrigger = basePath.includes('form');

			if (isFormTrigger || isLegacyFormTrigger) {
				const isTestWebhook = basePath.includes('test');
				res.status(404);
				return res.render('form-trigger-404', { isTestWebhook });
			}
		}

		if (error.errorCode === 409 && originalUrl && originalUrl.includes('form-waiting')) {
			//codes other than 200  breaks redirection to form-waiting page from form trigger
			//render form page instead of json
			return res.render('form-trigger-409', {
				message: error.message,
			});
		}

		httpStatusCode = error.httpStatusCode;

		if (error.errorCode) {
			response.code = error.errorCode;
		}
		if (error.hint) {
			response.hint = error.hint;
		}
		if (error.meta) {
			response.meta = error.meta;
		}
	}

	if (error instanceof NodeApiError) {
		if (inDevelopment) {
			Container.get(Logger).error([picocolors.red(error.name), error.message].join(' '));
		}

		Object.assign(response, error);
	}

	if (error.stack && inDevelopment) {
		response.stacktrace = error.stack;
	}

	res.status(httpStatusCode).json(response);
}

export const isUniqueConstraintError = (error: Error) =>
	['unique', 'duplicate'].some((s) => error.message.toLowerCase().includes(s));

export function reportError(error: Error) {
	if (!(error instanceof ResponseError) || error.httpStatusCode > 404) {
		Container.get(ErrorReporter).error(error);
	}
}

/**
 * A helper function which does not just allow to return Promises it also makes sure that
 * all the responses have the same format
 *
 *
 * @param {(req: Request, res: Response) => Promise<any>} processFunction The actual function to process the request
 */

export function send<T, R extends Request, S extends Response>(
	processFunction: (req: R, res: S) => Promise<T>,
	raw = false,
) {
	return async (req: R, res: S): Promise<void> => {
		try {
			const data = await processFunction(req, res);

			if (!res.headersSent) sendSuccessResponse(res, data, raw);
		} catch (error) {
			if (error instanceof Error) {
				reportError(error);

				if (isUniqueConstraintError(error)) {
					error.message = 'There is already an entry with this name';
				}
			}

			// eslint-disable-next-line @typescript-eslint/no-unsafe-argument
			sendErrorResponse(res, error);
		}
	};
}
