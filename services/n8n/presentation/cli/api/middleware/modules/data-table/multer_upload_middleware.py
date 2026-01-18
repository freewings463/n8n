"""
MIGRATION-META:
  source_path: packages/cli/src/modules/data-table/multer-upload-middleware.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/modules/data-table 的中间件。导入/依赖:外部:express、fs/promises、multer、nanoid；内部:@n8n/config、@n8n/di、@/errors/…/bad-request.error；本地:./data-table-size-validator.service、./data-table.repository、./utils/size-utils。导出:MulterUploadMiddleware。关键函数/方法:cb、ensureUploadDirExists、single、next。用于为该模块提供鉴权、拦截、上下文或统一异常处理。注释目标:eslint-disable id-denylist。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected Express RequestHandler-style middleware
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/data-table/multer-upload-middleware.ts -> services/n8n/presentation/cli/api/middleware/modules/data-table/multer_upload_middleware.py

/* eslint-disable id-denylist */
import { GlobalConfig } from '@n8n/config';
import { Service } from '@n8n/di';
import type { Request, RequestHandler } from 'express';
import { mkdir } from 'fs/promises';
import multer from 'multer';
import { nanoid } from 'nanoid';

import { BadRequestError } from '@/errors/response-errors/bad-request.error';

import { DataTableSizeValidator } from './data-table-size-validator.service';
import { DataTableRepository } from './data-table.repository';
import {
	type AuthenticatedRequestWithFile,
	type MulterDestinationCallback,
	type MulterFilenameCallback,
	type UploadMiddleware,
} from './types';
import { formatBytes } from './utils/size-utils';

const ALLOWED_MIME_TYPES = ['text/csv'];

@Service()
export class MulterUploadMiddleware implements UploadMiddleware {
	private upload: multer.Multer;

	private readonly uploadDir: string;

	constructor(
		private readonly globalConfig: GlobalConfig,
		private readonly sizeValidator: DataTableSizeValidator,
		private readonly dataTableRepository: DataTableRepository,
	) {
		this.uploadDir = this.globalConfig.dataTable.uploadDir;

		void this.ensureUploadDirExists();

		const storage = multer.diskStorage({
			destination: (_req: Request, _file: Express.Multer.File, cb: MulterDestinationCallback) => {
				cb(null, this.uploadDir);
			},
			filename: (_req: Request, _file: Express.Multer.File, cb: MulterFilenameCallback) => {
				const filename = nanoid(10);
				cb(null, filename);
			},
		});

		this.upload = multer({
			storage,
			limits: this.globalConfig.dataTable.uploadMaxFileSize
				? { fileSize: this.globalConfig.dataTable.uploadMaxFileSize }
				: undefined,
			fileFilter: async (req, file, cb: multer.FileFilterCallback) => {
				if (!ALLOWED_MIME_TYPES.includes(file.mimetype)) {
					cb(
						new BadRequestError(
							`Only the following file types are allowed: ${ALLOWED_MIME_TYPES.join(', ')}`,
						),
					);
					return;
				}

				const fileSize = parseInt(req.headers['content-length'] ?? '0', 10);

				// If uploadMaxFileSize is set, multer's limits will handle the rejection
				if (this.globalConfig.dataTable.uploadMaxFileSize) {
					cb(null, true);
					return;
				}

				// If uploadMaxFileSize is not set, check remaining space
				try {
					const sizeData = await this.sizeValidator.getCachedSizeData(async () => {
						return await this.dataTableRepository.findDataTablesSize();
					});
					const remainingSpace = Math.max(
						0,
						this.globalConfig.dataTable.maxSize - sizeData.totalBytes,
					);

					if (fileSize > remainingSpace) {
						const message =
							remainingSpace === 0
								? `Storage limit exceeded. Current usage: ${formatBytes(sizeData.totalBytes)}, Limit: ${formatBytes(this.globalConfig.dataTable.maxSize)}`
								: `File size exceeds remaining storage space. Available: ${formatBytes(remainingSpace)}, File: ${formatBytes(fileSize)}`;
						cb(new BadRequestError(message));
						return;
					}
					cb(null, true);
				} catch {
					cb(new BadRequestError('Failed to validate file size'));
				}
			},
		});
	}

	private async ensureUploadDirExists() {
		await mkdir(this.uploadDir, { recursive: true });
	}

	single(fieldName: string): RequestHandler {
		return (req, res, next) => {
			void this.upload.single(fieldName)(req, res, (error) => {
				if (error) {
					(req as AuthenticatedRequestWithFile).fileUploadError = error;
				}
				next();
			});
		};
	}
}
