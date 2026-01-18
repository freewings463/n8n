"""
MIGRATION-META:
  source_path: packages/cli/src/public-api/v1/handlers/source-control/source-control.handler.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/public-api/v1/handlers 的模块。导入/依赖:外部:express、simple-git；内部:@n8n/api-types、@n8n/db、@n8n/di、@/modules/…/source-control-preferences.service.ee、@/modules/…/source-control.service.ee、@/modules/…/import-result 等1项；本地:../middlewares/global.middleware。导出:无。关键函数/方法:apiKeyHasScopeWithGlobalScopeFallback、async。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/public-api/v1/handlers/source-control/source-control.handler.ts -> services/n8n/presentation/cli/api/public-api/v1/handlers/source-control/source_control_handler.py

import { PullWorkFolderRequestDto } from '@n8n/api-types';
import type { AuthenticatedRequest } from '@n8n/db';
import { Container } from '@n8n/di';
import type express from 'express';
import type { StatusResult } from 'simple-git';

import {
	getTrackingInformationFromPullResult,
	isSourceControlLicensed,
} from '@/modules/source-control.ee/source-control-helper.ee';
import { SourceControlPreferencesService } from '@/modules/source-control.ee/source-control-preferences.service.ee';
import { SourceControlService } from '@/modules/source-control.ee/source-control.service.ee';
import type { ImportResult } from '@/modules/source-control.ee/types/import-result';
import { EventService } from '@/events/event.service';

import { apiKeyHasScopeWithGlobalScopeFallback } from '../../shared/middlewares/global.middleware';

export = {
	pull: [
		apiKeyHasScopeWithGlobalScopeFallback({ scope: 'sourceControl:pull' }),
		async (
			req: AuthenticatedRequest,
			res: express.Response,
		): Promise<ImportResult | StatusResult | Promise<express.Response>> => {
			const sourceControlPreferencesService = Container.get(SourceControlPreferencesService);
			if (!isSourceControlLicensed()) {
				return res
					.status(401)
					.json({ status: 'Error', message: 'Source Control feature is not licensed' });
			}
			if (!sourceControlPreferencesService.isSourceControlConnected()) {
				return res
					.status(400)
					.json({ status: 'Error', message: 'Source Control is not connected to a repository' });
			}
			try {
				const payload = PullWorkFolderRequestDto.parse(req.body);
				const sourceControlService = Container.get(SourceControlService);
				const result = await sourceControlService.pullWorkfolder(req.user, payload);

				if (result.statusCode === 200) {
					Container.get(EventService).emit('source-control-user-pulled-api', {
						...getTrackingInformationFromPullResult(req.user.id, result.statusResult),
						forced: payload.force ?? false,
					});
					return res.status(200).send(result.statusResult);
				} else {
					return res.status(409).send(result.statusResult);
				}
			} catch (error) {
				return res.status(400).send((error as { message: string }).message);
			}
		},
	],
};
