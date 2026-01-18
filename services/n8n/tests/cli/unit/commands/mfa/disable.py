"""
MIGRATION-META:
  source_path: packages/cli/src/commands/mfa/disable.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/commands/mfa 的模块。导入/依赖:外部:zod；内部:@n8n/db、@n8n/decorators、@n8n/di；本地:../base-command。导出:DisableMFACommand。关键函数/方法:run、reportSuccess、reportUserDoesNotExistError。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/commands/mfa/disable.ts -> services/n8n/tests/cli/unit/commands/mfa/disable.py

import { UserRepository } from '@n8n/db';
import { Command } from '@n8n/decorators';
import { Container } from '@n8n/di';
import { z } from 'zod';

import { BaseCommand } from '../base-command';

const flagsSchema = z.object({
	email: z.string().describe('The email of the user to disable the MFA authentication'),
});

@Command({
	name: 'mfa:disable',
	description: 'Disable MFA authentication for a user',
	examples: ['--email=johndoe@example.com'],
	flagsSchema,
})
export class DisableMFACommand extends BaseCommand<z.infer<typeof flagsSchema>> {
	async run(): Promise<void> {
		const { flags } = this;

		if (!flags.email) {
			this.logger.info('An email with --email must be provided');
			return;
		}

		const repository = Container.get(UserRepository);
		const user = await repository.findOneBy({ email: flags.email });

		if (!user) {
			this.reportUserDoesNotExistError(flags.email);
			return;
		}

		if (
			user.mfaSecret === null &&
			Array.isArray(user.mfaRecoveryCodes) &&
			user.mfaRecoveryCodes.length === 0 &&
			!user.mfaEnabled
		) {
			this.reportUserDoesNotExistError(flags.email);
			return;
		}

		Object.assign(user, { mfaSecret: null, mfaRecoveryCodes: [], mfaEnabled: false });

		await repository.save(user);

		this.reportSuccess(flags.email);
	}

	async catch(error: Error) {
		this.logger.error('An error occurred while disabling MFA in account');
		this.logger.error(error.message);
	}

	private reportSuccess(email: string) {
		this.logger.info(`Successfully disabled MFA for user with email: ${email}`);
	}

	private reportUserDoesNotExistError(email: string) {
		this.logger.info(`User with email: ${email} does not exist`);
	}
}
