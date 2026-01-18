"""
MIGRATION-META:
  source_path: packages/cli/src/services/hooks.service.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/services 的服务。导入/依赖:外部:@rudderstack/rudder-sdk-node、express；内部:@n8n/di、@n8n/typeorm、@n8n/typeorm/…/QueryPartialEntity、@/auth/auth.service、@/interfaces、@/services/user.service；本地:无。导出:HooksService。关键函数/方法:inviteUsers、issueCookie、findOneUser、saveUser、updateSettings、workflowsCount、credentialsCount、settingsCount、authMiddleware、getRudderStackClient 等1项。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected Express RequestHandler-style middleware
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/services/hooks.service.ts -> services/n8n/presentation/cli/api/middleware/services/hooks_service.py

import type {
	AuthenticatedRequest,
	Settings,
	CredentialsEntity,
	User,
	WorkflowEntity,
} from '@n8n/db';
import {
	CredentialsRepository,
	WorkflowRepository,
	SettingsRepository,
	UserRepository,
} from '@n8n/db';
import { Service } from '@n8n/di';
// eslint-disable-next-line n8n-local-rules/misplaced-n8n-typeorm-import
import type { FindManyOptions, FindOneOptions, FindOptionsWhere } from '@n8n/typeorm';
import type { QueryDeepPartialEntity } from '@n8n/typeorm/query-builder/QueryPartialEntity';
import RudderStack, { type constructorOptions } from '@rudderstack/rudder-sdk-node';
import type { NextFunction, Response } from 'express';

import { AuthService } from '@/auth/auth.service';
import type { Invitation } from '@/interfaces';
import { UserService } from '@/services/user.service';

/**
 * Exposes functionality to be used by the cloud BE hooks.
 * DO NOT DELETE or RENAME any of the methods without making sure this is not used in cloud BE hooks.
 */
@Service()
export class HooksService {
	private innerAuthMiddleware: (
		req: AuthenticatedRequest,
		res: Response,
		next: NextFunction,
	) => Promise<void>;

	constructor(
		private readonly userService: UserService,
		private readonly authService: AuthService,
		private readonly userRepository: UserRepository,
		private readonly settingsRepository: SettingsRepository,
		private readonly workflowRepository: WorkflowRepository,
		private readonly credentialsRepository: CredentialsRepository,
	) {
		this.innerAuthMiddleware = authService.createAuthMiddleware({ allowSkipMFA: false });
	}

	/**
	 * Invite users to instance during signup
	 */
	async inviteUsers(owner: User, attributes: Invitation[]) {
		return await this.userService.inviteUsers(owner, attributes);
	}

	/**
	 * Set the n8n-auth cookie in the response to auto-login
	 * the user after instance is provisioned
	 */
	issueCookie(res: Response, user: User) {
		// TODO: The information on user has mfa enabled here, is missing!!
		// This could be a security problem!!
		// This is in just for the hackmation!!
		return this.authService.issueCookie(res, user, user.mfaEnabled);
	}

	/**
	 * Find user in the instance
	 * 1. To know whether the instance owner is already setup
	 * 2. To know when to update the user's profile also in cloud
	 */
	async findOneUser(filter: FindOneOptions<User>) {
		return await this.userRepository.findOne(filter);
	}

	/**
	 * Save instance owner with the cloud signup data
	 */
	async saveUser(user: User) {
		return await this.userRepository.save(user);
	}

	/**
	 * Update instance's settings
	 * 1. To keep the state when users are invited to the instance
	 */
	async updateSettings(filter: FindOptionsWhere<Settings>, set: QueryDeepPartialEntity<Settings>) {
		return await this.settingsRepository.update(filter, set);
	}

	/**
	 * Count the number of workflows
	 * 1. To enforce the active workflow limits in cloud
	 */
	async workflowsCount(filter: FindManyOptions<WorkflowEntity>) {
		return await this.workflowRepository.count(filter);
	}

	/**
	 * Count the number of credentials
	 * 1. To enforce the max credential limits in cloud
	 */
	async credentialsCount(filter: FindManyOptions<CredentialsEntity>) {
		return await this.credentialsRepository.count(filter);
	}

	/**
	 * Count the number of occurrences of a specific key
	 * 1. To know when to stop attempting to invite users
	 */
	async settingsCount(filter: FindManyOptions<Settings>) {
		return await this.settingsRepository.count(filter);
	}

	/**
	 * Add auth middleware to routes injected via the hooks
	 * 1. To authenticate the /proxy routes in the hooks
	 */
	async authMiddleware(req: AuthenticatedRequest, res: Response, next: NextFunction) {
		return await this.innerAuthMiddleware(req, res, next);
	}

	getRudderStackClient(key: string, options: constructorOptions): RudderStack {
		return new RudderStack(key, options);
	}

	/**
	 * Return repositories to be used in the hooks
	 * 1. Some self-hosted users rely in the repositories to interact with the DB directly
	 */
	dbCollections() {
		return {
			User: this.userRepository,
			Settings: this.settingsRepository,
			Credentials: this.credentialsRepository,
			Workflow: this.workflowRepository,
		};
	}
}
