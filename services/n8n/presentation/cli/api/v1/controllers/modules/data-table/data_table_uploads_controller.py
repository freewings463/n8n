"""
MIGRATION-META:
  source_path: packages/cli/src/modules/data-table/data-table-uploads.controller.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/modules/data-table 的控制器。导入/依赖:外部:multer；内部:@n8n/decorators、@n8n/di、@/errors/…/bad-request.error；本地:./csv-parser.service、./multer-upload-middleware、./types。导出:DataTableUploadsController。关键函数/方法:uploadFile、hasStringProperty。用于处理该模块接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected @RestController/@Controller from @n8n/decorators
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/data-table/data-table-uploads.controller.ts -> services/n8n/presentation/cli/api/v1/controllers/modules/data-table/data_table_uploads_controller.py

import { Post, RestController } from '@n8n/decorators';
import { Container } from '@n8n/di';
import multer from 'multer';

import { BadRequestError } from '@/errors/response-errors/bad-request.error';

import { CsvParserService } from './csv-parser.service';
import { MulterUploadMiddleware } from './multer-upload-middleware';
import { AuthenticatedRequestWithFile, hasStringProperty } from './types';

const uploadMiddleware = Container.get(MulterUploadMiddleware);

@RestController('/data-tables/uploads')
export class DataTableUploadsController {
	constructor(private readonly csvParserService: CsvParserService) {}

	@Post('/', {
		middlewares: [uploadMiddleware.single('file')],
	})
	async uploadFile(req: AuthenticatedRequestWithFile, _res: Response) {
		if (req.fileUploadError) {
			const error = req.fileUploadError;
			if (error instanceof multer.MulterError) {
				throw new BadRequestError(`File upload error: ${error.message}`);
			} else if (error instanceof BadRequestError) {
				throw error;
			} else {
				throw new BadRequestError('File upload failed');
			}
		}

		if (!req.file) {
			throw new BadRequestError('No file uploaded');
		}

		// Extract hasHeaders parameter from request body (multer parses form fields to body), default to true
		const hasHeaders =
			hasStringProperty(req.body, 'hasHeaders') && req.body.hasHeaders === 'false' ? false : true;

		const metadata = await this.csvParserService.parseFile(req.file.filename, hasHeaders);

		return {
			originalName: req.file.originalname,
			id: req.file.filename,
			rowCount: metadata.rowCount,
			columnCount: metadata.columnCount,
			columns: metadata.columns,
		};
	}
}
