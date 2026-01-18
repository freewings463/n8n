"""
MIGRATION-META:
  source_path: packages/cli/src/commands/user-management/reset.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/commands/user-management 的模块。导入/依赖:外部:无；内部:@n8n/db、@n8n/decorators、@n8n/di；本地:../base-command。导出:Reset。关键函数/方法:run、getInstanceOwner。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - CLI command -> presentation/cli/commands
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/commands/user-management/reset.ts -> services/n8n/presentation/cli/cli/commands/user-management/reset.py

import type { CredentialsEntity } from '@n8n/db';
import {
	User,
	CredentialsRepository,
	ProjectRepository,
	SharedCredentialsRepository,
	SharedWorkflowRepository,
	UserRepository,
	GLOBAL_OWNER_ROLE,
} from '@n8n/db';
import { Command } from '@n8n/decorators';
import { Container } from '@n8n/di';

import { BaseCommand } from '../base-command';

const defaultUserProps = {
	firstName: null,
	lastName: null,
	email: null,
	password: null,
	lastActiveAt: null,
	role: 'global:owner',
};

@Command({
	name: 'user-management:reset',
	description: 'Resets the database to the default user state',
})
export class Reset extends BaseCommand {
	async run(): Promise<void> {
		const owner = await this.getInstanceOwner();
		const personalProject = await Container.get(ProjectRepository).getPersonalProjectForUserOrFail(
			owner.id,
		);

		await Container.get(SharedWorkflowRepository).makeOwnerOfAllWorkflows(personalProject);
		await Container.get(SharedCredentialsRepository).makeOwnerOfAllCredentials(personalProject);

		await Container.get(UserRepository).deleteAllExcept(owner);
		await Container.get(UserRepository).save(Object.assign(owner, defaultUserProps));

		const danglingCredentials: CredentialsEntity[] = await Container.get(CredentialsRepository)
			.createQueryBuilder('credentials')
			.leftJoinAndSelect('credentials.shared', 'shared')
			.where('shared.credentialsId is null')
			.getMany();
		const newSharedCredentials = danglingCredentials.map((credentials) =>
			Container.get(SharedCredentialsRepository).create({
				credentials,
				projectId: personalProject.id,
				role: 'credential:owner',
			}),
		);
		await Container.get(SharedCredentialsRepository).save(newSharedCredentials);

		this.logger.info('Successfully reset the database to default user state.');
	}

	async getInstanceOwner(): Promise<User> {
		const owner = await Container.get(UserRepository).findOneBy({
			role: { slug: GLOBAL_OWNER_ROLE.slug },
		});

		if (owner) return owner;

		const user = new User();

		Object.assign(user, defaultUserProps);

		await Container.get(UserRepository).save(user);

		return await Container.get(UserRepository).findOneByOrFail({
			role: { slug: GLOBAL_OWNER_ROLE.slug },
		});
	}

	async catch(error: Error): Promise<void> {
		this.logger.error('Error resetting database. See log messages for details.');
		this.logger.error(error.message);
		process.exit(1);
	}
}
