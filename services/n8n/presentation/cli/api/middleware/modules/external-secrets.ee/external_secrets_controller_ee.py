"""
MIGRATION-META:
  source_path: packages/cli/src/modules/external-secrets.ee/external-secrets.controller.ee.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/modules/external-secrets.ee 的控制器。导入/依赖:外部:express；内部:@n8n/backend-common、@n8n/decorators 等1项；本地:./external-secrets-providers.ee、./external-secrets.service.ee、./types。导出:ExternalSecretsController。关键函数/方法:validateProviderName、next、getProviders、getProvider、testProviderSettings、setProviderSettings、setProviderConnected、updateProvider、getSecretNames。用于处理该模块接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected Express RequestHandler-style middleware
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/external-secrets.ee/external-secrets.controller.ee.ts -> services/n8n/presentation/cli/api/middleware/modules/external-secrets.ee/external_secrets_controller_ee.py

import { Logger } from '@n8n/backend-common';
import { Get, Post, RestController, GlobalScope, Middleware } from '@n8n/decorators';
import { Request, Response, NextFunction } from 'express';

import { NotFoundError } from '@/errors/response-errors/not-found.error';

import { ExternalSecretsProviders } from './external-secrets-providers.ee';
import { ExternalSecretsService } from './external-secrets.service.ee';
import { ExternalSecretsRequest } from './types';

@RestController('/external-secrets')
export class ExternalSecretsController {
	constructor(
		private readonly secretsService: ExternalSecretsService,
		private readonly secretsProviders: ExternalSecretsProviders,
		private readonly logger: Logger,
	) {
		this.logger = this.logger.scoped('external-secrets');
	}

	@Middleware()
	validateProviderName(req: Request, _: Response, next: NextFunction) {
		if ('provider' in req.params) {
			const { provider } = req.params;
			if (!this.secretsProviders.hasProvider(provider)) {
				throw new NotFoundError(`Could not find provider "${provider}"`);
			}
		}
		next();
	}

	@Get('/providers')
	@GlobalScope('externalSecretsProvider:list')
	async getProviders() {
		return this.secretsService.getProviders();
	}

	@Get('/providers/:provider')
	@GlobalScope('externalSecretsProvider:read')
	async getProvider(req: ExternalSecretsRequest.GetProvider) {
		const providerName = req.params.provider;
		return this.secretsService.getProvider(providerName);
	}

	@Post('/providers/:provider/test')
	@GlobalScope('externalSecretsProvider:read')
	async testProviderSettings(req: ExternalSecretsRequest.TestProviderSettings, res: Response) {
		const providerName = req.params.provider;
		const result = await this.secretsService.testProviderSettings(providerName, req.body);
		if (result.success) {
			res.statusCode = 200;
		} else {
			res.statusCode = 400;
		}
		return result;
	}

	@Post('/providers/:provider')
	@GlobalScope('externalSecretsProvider:create')
	async setProviderSettings(req: ExternalSecretsRequest.SetProviderSettings) {
		const providerName = req.params.provider;
		await this.secretsService.saveProviderSettings(providerName, req.body, req.user.id);
		return {};
	}

	@Post('/providers/:provider/connect')
	@GlobalScope('externalSecretsProvider:update')
	async setProviderConnected(req: ExternalSecretsRequest.SetProviderConnected) {
		const providerName = req.params.provider;
		await this.secretsService.saveProviderConnected(providerName, req.body.connected);
		return {};
	}

	@Post('/providers/:provider/update')
	@GlobalScope('externalSecretsProvider:sync')
	async updateProvider(req: ExternalSecretsRequest.UpdateProvider, res: Response) {
		const providerName = req.params.provider;
		try {
			await this.secretsService.updateProvider(providerName);
			return { updated: true };
		} catch (error) {
			this.logger.error('Error updating provider', { providerName, error });
			res.statusCode = 400;
			return { updated: false };
		}
	}

	@Get('/secrets')
	@GlobalScope('externalSecret:list')
	getSecretNames() {
		return this.secretsService.getAllSecrets();
	}
}
