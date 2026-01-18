"""
MIGRATION-META:
  source_path: packages/cli/src/public-api/v1/handlers/variables/variables.handler.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/public-api/v1/handlers 的模块。导入/依赖:外部:express；内部:@n8n/api-types、@n8n/db、@n8n/di、@n8n/typeorm、@/environments.ee/…/variables.controller.ee、@/requests；本地:../services/pagination.service。导出:无。关键函数/方法:isLicensed、apiKeyHasScopeWithGlobalScopeFallback、async。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/public-api/v1/handlers/variables/variables.handler.ts -> services/n8n/presentation/cli/api/public-api/v1/handlers/variables/variables_handler.py

import { CreateVariableRequestDto } from '@n8n/api-types';
import type { AuthenticatedRequest } from '@n8n/db';
import { VariablesRepository } from '@n8n/db';
import { Container } from '@n8n/di';
// eslint-disable-next-line n8n-local-rules/misplaced-n8n-typeorm-import
import { IsNull } from '@n8n/typeorm';
import type { Response } from 'express';

import {
	apiKeyHasScopeWithGlobalScopeFallback,
	isLicensed,
	validCursor,
} from '../../shared/middlewares/global.middleware';
import { encodeNextCursor } from '../../shared/services/pagination.service';

import { VariablesController } from '@/environments.ee/variables/variables.controller.ee';
import type { VariablesRequest } from '@/requests';

export = {
	createVariable: [
		isLicensed('feat:variables'),
		apiKeyHasScopeWithGlobalScopeFallback({ scope: 'variable:create' }),
		async (req: AuthenticatedRequest, res: Response) => {
			const payload = CreateVariableRequestDto.safeParse(req.body);
			if (payload.error) {
				return res.status(400).json(payload.error.errors[0]);
			}
			await Container.get(VariablesController).createVariable(req, res, payload.data);

			return res.status(201).send();
		},
	],
	updateVariable: [
		isLicensed('feat:variables'),
		apiKeyHasScopeWithGlobalScopeFallback({ scope: 'variable:update' }),
		async (req: AuthenticatedRequest<{ id: string }>, res: Response) => {
			const payload = CreateVariableRequestDto.safeParse(req.body);
			if (payload.error) {
				return res.status(400).json(payload.error.errors[0]);
			}
			await Container.get(VariablesController).updateVariable(req, res, payload.data);

			return res.status(204).send();
		},
	],
	deleteVariable: [
		isLicensed('feat:variables'),
		apiKeyHasScopeWithGlobalScopeFallback({ scope: 'variable:delete' }),
		async (req: AuthenticatedRequest<{ id: string }>, res: Response) => {
			await Container.get(VariablesController).deleteVariable(req);

			return res.status(204).send();
		},
	],
	getVariables: [
		isLicensed('feat:variables'),
		apiKeyHasScopeWithGlobalScopeFallback({ scope: 'variable:list' }),
		validCursor,
		async (req: VariablesRequest.GetAll, res: Response) => {
			const { offset = 0, limit = 100, projectId, state } = req.query;

			const [variables, count] = await Container.get(VariablesRepository).findAndCount({
				skip: offset,
				take: limit,
				where: {
					project: projectId === 'null' ? IsNull() : { id: projectId },
					value: state === 'empty' ? '' : undefined,
				},
				relations: ['project'],
			});

			return res.json({
				data: variables,
				nextCursor: encodeNextCursor({
					offset,
					limit,
					numberOfTotalRecords: count,
				}),
			});
		},
	],
};
