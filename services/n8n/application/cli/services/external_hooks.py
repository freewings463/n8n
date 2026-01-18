"""
MIGRATION-META:
  source_path: packages/cli/src/external-hooks.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src 的模块。导入/依赖:外部:oauth-1.0a；内部:@n8n/api-types、@n8n/backend-common、@n8n/client-oauth2、@n8n/config、@n8n/db、@n8n/di 等4项；本地:无。导出:ExternalHooks。关键函数/方法:init、loadHooks。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/external-hooks.ts -> services/n8n/application/cli/services/external_hooks.py

import type { FrontendSettings, UserUpdateRequestDto } from '@n8n/api-types';
import { Logger } from '@n8n/backend-common';
import type { ClientOAuth2Options } from '@n8n/client-oauth2';
import { GlobalConfig } from '@n8n/config';
import type { TagEntity, User, ICredentialsDb, PublicUser } from '@n8n/db';
import {
	CredentialsRepository,
	WorkflowRepository,
	SettingsRepository,
	UserRepository,
} from '@n8n/db';
import { Service } from '@n8n/di';
import { ErrorReporter } from 'n8n-core';
import type { IRun, IWorkflowBase, Workflow, WorkflowExecuteMode } from 'n8n-workflow';
import { UnexpectedError } from 'n8n-workflow';
import type clientOAuth1 from 'oauth-1.0a';

import type { AbstractServer } from '@/abstract-server';
import type { Config } from '@/config';

type Repositories = {
	User: UserRepository;
	Settings: SettingsRepository;
	Credentials: CredentialsRepository;
	Workflow: WorkflowRepository;
};

type ExternalHooksMap = {
	'n8n.ready': [server: AbstractServer, config: Config];
	'n8n.stop': never;
	'worker.ready': never;

	'activeWorkflows.initialized': never;

	'credentials.create': [encryptedData: ICredentialsDb];
	'credentials.update': [newCredentialData: ICredentialsDb];
	'credentials.delete': [credentialId: string];

	'frontend.settings': [frontendSettings: FrontendSettings];

	'mfa.beforeSetup': [user: User];

	'oauth1.authenticate': [
		oAuthOptions: clientOAuth1.Options,
		oauthRequestData: { oauth_callback: string },
	];
	'oauth2.authenticate': [oAuthOptions: ClientOAuth2Options];
	'oauth2.callback': [oAuthOptions: ClientOAuth2Options];
	'oauth2.dynamicClientRegistration': [registerPayload: { redirect_uris: string[] }];

	'tag.beforeCreate': [tag: TagEntity];
	'tag.afterCreate': [tag: TagEntity];
	'tag.beforeUpdate': [tag: TagEntity];
	'tag.afterUpdate': [tag: TagEntity];
	'tag.beforeDelete': [tagId: string];
	'tag.afterDelete': [tagId: string];

	'user.deleted': [user: PublicUser];
	'user.profile.beforeUpdate': [
		userId: string,
		currentEmail: string,
		payload: UserUpdateRequestDto,
	];
	'user.profile.update': [currentEmail: string, publicUser: PublicUser];
	'user.password.update': [updatedEmail: string, updatedPassword: string | null];
	'user.invited': [emails: string[]];

	'workflow.create': [createdWorkflow: IWorkflowBase];
	'workflow.afterCreate': [createdWorkflow: IWorkflowBase];
	'workflow.activate': [updatedWorkflow: IWorkflowBase];
	'workflow.update': [updatedWorkflow: IWorkflowBase];
	'workflow.afterUpdate': [updatedWorkflow: IWorkflowBase];
	'workflow.delete': [workflowId: string];
	'workflow.afterDelete': [workflowId: string];
	'workflow.afterArchive': [workflowId: string];
	'workflow.afterUnarchive': [workflowId: string];

	'workflow.preExecute': [workflow: Workflow, mode: WorkflowExecuteMode];
	'workflow.postExecute': [
		fullRunData: IRun | undefined,
		workflowData: IWorkflowBase,
		executionId: string,
	];
};
type HookNames = keyof ExternalHooksMap;

// TODO: Derive this type from Hooks
interface IExternalHooksFileData {
	[Resource: string]: {
		[Operation: string]: Array<(...args: unknown[]) => Promise<void>>;
	};
}

@Service()
export class ExternalHooks {
	private readonly registered: {
		[hookName in HookNames]?: Array<(...args: ExternalHooksMap[hookName]) => Promise<void>>;
	} = {};

	private readonly dbCollections: Repositories;

	constructor(
		private readonly logger: Logger,
		private readonly errorReporter: ErrorReporter,
		private readonly globalConfig: GlobalConfig,
		userRepository: UserRepository,
		settingsRepository: SettingsRepository,
		credentialsRepository: CredentialsRepository,
		workflowRepository: WorkflowRepository,
	) {
		this.dbCollections = {
			User: userRepository,
			Settings: settingsRepository,
			Credentials: credentialsRepository,
			Workflow: workflowRepository,
		};
	}

	async init() {
		const externalHookFiles = this.globalConfig.externalHooks.files;

		// Load all the provided hook-files
		for (let hookFilePath of externalHookFiles) {
			hookFilePath = hookFilePath.trim();
			try {
				const hookFile = require(hookFilePath) as IExternalHooksFileData;
				this.loadHooks(hookFile);
			} catch (e) {
				const error = e instanceof Error ? e : new Error(`${e}`);

				throw new UnexpectedError('Problem loading external hook file', {
					extra: { errorMessage: error.message, hookFilePath },
					cause: error,
				});
			}
		}
	}

	private loadHooks(hookFileData: IExternalHooksFileData) {
		const { registered } = this;
		for (const [resource, operations] of Object.entries(hookFileData)) {
			for (const operation of Object.keys(operations)) {
				const hookName = `${resource}.${operation}` as HookNames;
				registered[hookName] ??= [];
				registered[hookName].push(...operations[operation]);
			}
		}
	}

	async run<HookName extends HookNames>(
		hookName: HookName,
		hookParameters?: ExternalHooksMap[HookName],
	): Promise<void> {
		const { registered, dbCollections } = this;
		const hookFunctions = registered[hookName];
		if (!hookFunctions?.length) return;

		const context = { dbCollections };

		for (const hookFunction of hookFunctions) {
			try {
				await hookFunction.apply(context, hookParameters);
			} catch (cause) {
				this.logger.error(`There was a problem running hook "${hookName}"`);

				const error = new UnexpectedError(`External hook "${hookName}" failed`, { cause });
				this.errorReporter.error(error, { level: 'fatal' });

				// Throw original error, so that hooks control the error returned to use
				// For example on Cloud we return upgrade message when user reaches max executions or activations
				throw cause;
			}
		}
	}
}
