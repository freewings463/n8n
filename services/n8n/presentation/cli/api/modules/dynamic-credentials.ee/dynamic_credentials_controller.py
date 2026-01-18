"""
MIGRATION-META:
  source_path: packages/cli/src/modules/dynamic-credentials.ee/dynamic-credentials.controller.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/modules/dynamic-credentials.ee 的控制器。导入/依赖:外部:express；内部:@n8n/decorators、@/credentials/credentials.service.ee、@/errors/…/not-found.error、@/errors/…/bad-request.error、@/oauth/oauth.service、@n8n/db 等2项；本地:../repositories/credential-resolver.repository、./services、./utils。导出:DynamicCredentialsController。关键函数/方法:authorizeCredential。用于处理该模块接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/dynamic-credentials.ee/dynamic-credentials.controller.ts -> services/n8n/presentation/cli/api/modules/dynamic-credentials.ee/dynamic_credentials_controller.py

import { Post, RestController } from '@n8n/decorators';
import { Request, Response } from 'express';

import { EnterpriseCredentialsService } from '@/credentials/credentials.service.ee';
import { NotFoundError } from '@/errors/response-errors/not-found.error';
import { BadRequestError } from '@/errors/response-errors/bad-request.error';
import { CreateCsrfStateData, OauthService } from '@/oauth/oauth.service';
import { CredentialsEntity } from '@n8n/db';
import { DynamicCredentialResolverRepository } from './database/repositories/credential-resolver.repository';
import { DynamicCredentialResolverRegistry } from './services';
import { getBearerToken } from './utils';
import { Cipher } from 'n8n-core';
import { jsonParse } from 'n8n-workflow';

@RestController('/credentials')
export class DynamicCredentialsController {
	constructor(
		private readonly enterpriseCredentialsService: EnterpriseCredentialsService,
		private readonly oauthService: OauthService,
		private readonly resolverRepository: DynamicCredentialResolverRepository,
		private readonly resolverRegistry: DynamicCredentialResolverRegistry,
		private readonly cipher: Cipher,
	) {}

	@Post('/:id/authorize', { skipAuth: true })
	async authorizeCredential(req: Request, _res: Response): Promise<string> {
		const credential = await this.enterpriseCredentialsService.getOne(req.params.id);
		const token = getBearerToken(req);

		if (!credential) {
			throw new NotFoundError('Credential not found');
		}

		if (!credential.type.includes('OAuth2') && !credential.type.includes('OAuth1')) {
			throw new BadRequestError('Credential type not supported');
		}

		const resolverId = req.query.resolverId as string | undefined;
		if (!resolverId) {
			throw new BadRequestError('Missing resolverId query parameter');
		}

		const resolverEntity = await this.resolverRepository.findOneBy({
			id: resolverId,
		});

		if (!resolverEntity) {
			throw new NotFoundError('Resolver not found');
		}

		// Get resolver instance from registry
		const resolver = this.resolverRegistry.getResolverByTypename(resolverEntity.type);

		if (!resolver) {
			throw new NotFoundError('Resolver type not found');
		}

		if (resolver.validateIdentity) {
			// Decrypt and parse resolver configuration
			const decryptedConfig = this.cipher.decrypt(resolverEntity.config);
			const resolverConfig = jsonParse<Record<string, unknown>>(decryptedConfig);

			await resolver.validateIdentity(token, {
				resolverId,
				resolverName: resolverEntity.type,
				configuration: resolverConfig,
			});
		}

		const callerData: [CredentialsEntity, CreateCsrfStateData] = [
			credential,
			{
				cid: credential.id,
				origin: 'dynamic-credential',
				authorizationHeader: req.headers.authorization ?? '',
				credentialResolverId: req.query.resolverId,
			},
		];

		if (credential.type.includes('OAuth2')) {
			return await this.oauthService.generateAOauth2AuthUri(...callerData);
		}

		if (credential.type.includes('OAuth1')) {
			return await this.oauthService.generateAOauth1AuthUri(...callerData);
		}

		throw new BadRequestError('Credential type not supported');
	}
}
