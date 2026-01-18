"""
MIGRATION-META:
  source_path: packages/cli/src/modules/chat-hub/chat-hub-credentials.service.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/modules/chat-hub 的服务。导入/依赖:外部:无；内部:@n8n/db、@n8n/di、@n8n/typeorm、n8n-workflow、@/credentials/credentials-finder.service、@/credentials/credentials.service 等2项；本地:无。导出:ChatHubCredentialsService。关键函数/方法:ensureCredentialAccess、pickCredentialId、findPersonalProject、findProviderCredential、findWorkflowCredentialAndProject。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected TypeORM Repository/EntityManager usage
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/chat-hub/chat-hub-credentials.service.ts -> services/n8n/infrastructure/cli/persistence/repositories/modules/chat-hub/chat_hub_credentials_service.py

import {
	ChatHubLLMProvider,
	PROVIDER_CREDENTIAL_TYPE_MAP,
	type ChatHubConversationModel,
} from '@n8n/api-types';
import { ProjectRepository, SharedWorkflowRepository, User } from '@n8n/db';
import { Service } from '@n8n/di';
import { EntityManager } from '@n8n/typeorm';
import type { INodeCredentials } from 'n8n-workflow';

import { CredentialsFinderService } from '@/credentials/credentials-finder.service';
import { CredentialsService } from '@/credentials/credentials.service';
import { BadRequestError } from '@/errors/response-errors/bad-request.error';
import { ForbiddenError } from '@/errors/response-errors/forbidden.error';

@Service()
export class ChatHubCredentialsService {
	constructor(
		private readonly credentialsService: CredentialsService,
		private readonly sharedWorkflowRepository: SharedWorkflowRepository,
		private readonly credentialsFinderService: CredentialsFinderService,
		private readonly projectRepository: ProjectRepository,
	) {}

	async ensureCredentialAccess(user: User, credentialId: string) {
		const credential = await this.credentialsFinderService.findCredentialForUser(
			credentialId,
			user,
			['credential:read'],
		);
		if (!credential) {
			throw new ForbiddenError("You don't have access to the provided credentials");
		}

		return credential;
	}

	private pickCredentialId(
		provider: ChatHubConversationModel['provider'],
		credentials: INodeCredentials,
	): string | null {
		if (provider === 'n8n' || provider === 'custom-agent') {
			return null;
		}

		return credentials[PROVIDER_CREDENTIAL_TYPE_MAP[provider]]?.id ?? null;
	}

	async findPersonalProject(user: User, trx?: EntityManager) {
		const project = await this.projectRepository.getPersonalProjectForUser(user.id, trx);
		if (!project) {
			throw new ForbiddenError('Missing personal project');
		}
		return project;
	}

	/**
	 * Only checks if the expected credential for the provider is present in the credentials object.
	 * Doesn't check access rights or existence in DB, those are checked by CredentialsPermissionChecker
	 * at execution time within the context and project of the workflow.
	 */
	findProviderCredential(provider: ChatHubLLMProvider, credentials: INodeCredentials) {
		const credentialId = this.pickCredentialId(provider, credentials);
		if (!credentialId) {
			throw new BadRequestError('No credentials provided for the selected model provider');
		}

		return credentialId;
	}

	async findWorkflowCredentialAndProject(
		provider: ChatHubLLMProvider,
		credentials: INodeCredentials,
		workflowId: string,
	) {
		const credentialId = this.pickCredentialId(provider, credentials);
		if (!credentialId) {
			throw new BadRequestError('No credentials provided for the selected model provider');
		}

		const project = await this.sharedWorkflowRepository.getWorkflowOwningProject(workflowId);
		if (!project) {
			throw new ForbiddenError('Missing owner project for the workflow');
		}

		const workflowCredentials =
			await this.credentialsService.findAllCredentialIdsForWorkflow(workflowId);
		const globalCredentials = await this.credentialsService.findAllGlobalCredentialIds();
		workflowCredentials.push.apply(workflowCredentials, globalCredentials);

		const credential = workflowCredentials.find((c) => c.id === credentialId);
		if (!credential) {
			throw new ForbiddenError("You don't have access to the provided credentials");
		}

		return {
			credentialId: credential.id,
			projectId: project.id,
		};
	}
}
