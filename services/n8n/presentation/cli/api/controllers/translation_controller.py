"""
MIGRATION-META:
  source_path: packages/cli/src/controllers/translation.controller.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/controllers 的控制器。导入/依赖:外部:express、fs/promises；内部:@/constants、@n8n/backend-common、@n8n/config、@n8n/decorators、@/credential-types、@/errors/…/bad-request.error 等1项；本地:无。导出:CREDENTIAL_TRANSLATIONS_DIR、NODE_HEADERS_PATH、Credential、TranslationController。关键函数/方法:getCredentialTranslation、getNodeTranslationHeaders。用于处理该模块接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/controllers/translation.controller.ts -> services/n8n/presentation/cli/api/controllers/translation_controller.py

import { NODES_BASE_DIR } from '@/constants';
import { safeJoinPath } from '@n8n/backend-common';
import { GlobalConfig } from '@n8n/config';
import { Get, RestController } from '@n8n/decorators';
import type { Request } from 'express';
import { access } from 'fs/promises';

import { CredentialTypes } from '@/credential-types';
import { BadRequestError } from '@/errors/response-errors/bad-request.error';
import { InternalServerError } from '@/errors/response-errors/internal-server.error';

export const CREDENTIAL_TRANSLATIONS_DIR = 'n8n-nodes-base/dist/credentials/translations';
export const NODE_HEADERS_PATH = safeJoinPath(NODES_BASE_DIR, 'dist/nodes/headers');

export declare namespace TranslationRequest {
	export type Credential = Request<{}, {}, {}, { credentialType: string }>;
}

@RestController('/')
export class TranslationController {
	constructor(
		private readonly credentialTypes: CredentialTypes,
		private readonly globalConfig: GlobalConfig,
	) {}

	@Get('/credential-translation')
	async getCredentialTranslation(req: TranslationRequest.Credential) {
		const { credentialType } = req.query;

		if (!this.credentialTypes.recognizes(credentialType))
			throw new BadRequestError(`Invalid Credential type: "${credentialType}"`);

		const { defaultLocale } = this.globalConfig;
		const translationPath = safeJoinPath(
			CREDENTIAL_TRANSLATIONS_DIR,
			defaultLocale,
			`${credentialType}.json`,
		);

		try {
			// eslint-disable-next-line @typescript-eslint/no-unsafe-return
			return require(translationPath);
		} catch (error) {
			return null;
		}
	}

	@Get('/node-translation-headers')
	async getNodeTranslationHeaders() {
		try {
			await access(`${NODE_HEADERS_PATH}.js`);
		} catch {
			return; // no headers available
		}

		try {
			// eslint-disable-next-line @typescript-eslint/no-unsafe-return
			return require(NODE_HEADERS_PATH);
		} catch (error) {
			throw new InternalServerError('Failed to load headers file', error);
		}
	}
}
