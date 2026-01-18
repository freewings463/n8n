"""
MIGRATION-META:
  source_path: packages/cli/src/commands/import/credentials.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/commands/import 的模块。导入/依赖:外部:fast-glob、zod；内部:@n8n/decorators、@n8n/di、@n8n/permissions、@n8n/typeorm、n8n-core、n8n-workflow 等1项；本地:../base-command。导出:ImportCredentialsCommand。关键函数/方法:run、reportSuccess、storeCredential、checkRelations、readCredentials、getCredentialOwner、credentialExists、getProject。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/commands/import/credentials.ts -> services/n8n/tests/cli/unit/commands/import/credentials.py

import {
	CredentialsEntity,
	Project,
	User,
	SharedCredentials,
	ProjectRepository,
	GLOBAL_OWNER_ROLE,
} from '@n8n/db';
import { Command } from '@n8n/decorators';
import { Container } from '@n8n/di';
import { PROJECT_OWNER_ROLE_SLUG } from '@n8n/permissions';
// eslint-disable-next-line n8n-local-rules/misplaced-n8n-typeorm-import
import type { EntityManager } from '@n8n/typeorm';
import glob from 'fast-glob';
import fs from 'fs';
import { Cipher } from 'n8n-core';
import type { ICredentialsEncrypted } from 'n8n-workflow';
import { jsonParse, UserError } from 'n8n-workflow';
import { z } from 'zod';

import { BaseCommand } from '../base-command';

import { UM_FIX_INSTRUCTION } from '@/constants';

const flagsSchema = z.object({
	input: z
		.string()
		.alias('i')
		.describe('Input file name or directory if --separate is used')
		.optional(),
	separate: z
		.boolean()
		.default(false)
		.describe('Imports *.json files from directory provided by --input'),
	userId: z
		.string()
		.describe('The ID of the user to assign the imported credentials to')
		.optional(),
	projectId: z
		.string()
		.describe('The ID of the project to assign the imported credential to')
		.optional(),
});

@Command({
	name: 'import:credentials',
	description: 'Import credentials',
	examples: [
		'--input=file.json',
		'--separate --input=backups/latest/',
		'--input=file.json --userId=1d64c3d2-85fe-4a83-a649-e446b07b3aae',
		'--input=file.json --projectId=Ox8O54VQrmBrb4qL',
		'--separate --input=backups/latest/ --userId=1d64c3d2-85fe-4a83-a649-e446b07b3aae',
	],
	flagsSchema,
})
export class ImportCredentialsCommand extends BaseCommand<z.infer<typeof flagsSchema>> {
	private transactionManager: EntityManager;

	async run(): Promise<void> {
		const { flags } = this;

		if (!flags.input) {
			this.logger.info('An input file or directory with --input must be provided');
			return;
		}

		if (flags.separate) {
			if (fs.existsSync(flags.input)) {
				if (!fs.lstatSync(flags.input).isDirectory()) {
					this.logger.info('The argument to --input must be a directory');
					return;
				}
			}
		}

		if (flags.projectId && flags.userId) {
			throw new UserError(
				'You cannot use `--userId` and `--projectId` together. Use one or the other.',
			);
		}

		const credentials = await this.readCredentials(flags.input, flags.separate);

		const { manager: dbManager } = Container.get(ProjectRepository);
		await dbManager.transaction(async (transactionManager) => {
			this.transactionManager = transactionManager;

			const project = await this.getProject(flags.userId, flags.projectId);

			const result = await this.checkRelations(credentials, flags.projectId, flags.userId);

			if (!result.success) {
				throw new UserError(result.message);
			}

			for (const credential of credentials) {
				await this.storeCredential(credential, project);
			}
		});

		this.reportSuccess(credentials.length);
	}

	async catch(error: Error) {
		this.logger.error(
			'An error occurred while importing credentials. See log messages for details.',
		);
		this.logger.error(error.message);
	}

	private reportSuccess(total: number) {
		this.logger.info(
			`Successfully imported ${total} ${total === 1 ? 'credential.' : 'credentials.'}`,
		);
	}

	private async storeCredential(credential: Partial<CredentialsEntity>, project: Project) {
		const result = await this.transactionManager.upsert(CredentialsEntity, credential, ['id']);

		const sharingExists = await this.transactionManager.existsBy(SharedCredentials, {
			credentialsId: credential.id,
			role: 'credential:owner',
		});

		if (!sharingExists) {
			await this.transactionManager.upsert(
				SharedCredentials,
				{
					credentialsId: result.identifiers[0].id as string,
					role: 'credential:owner',
					projectId: project.id,
				},
				['credentialsId', 'projectId'],
			);
		}
	}

	private async checkRelations(
		credentials: ICredentialsEncrypted[],
		projectId?: string,
		userId?: string,
	) {
		// The credential is not supposed to be re-owned.
		if (!projectId && !userId) {
			return {
				success: true as const,
				message: undefined,
			};
		}

		for (const credential of credentials) {
			if (credential.id === undefined) {
				continue;
			}

			if (!(await this.credentialExists(credential.id))) {
				continue;
			}

			const { user, project: ownerProject } = await this.getCredentialOwner(credential.id);

			if (!ownerProject) {
				continue;
			}

			if (ownerProject.id !== projectId) {
				const currentOwner =
					ownerProject.type === 'personal'
						? `the user with the ID "${user.id}"`
						: `the project with the ID "${ownerProject.id}"`;
				const newOwner = userId
					? // The user passed in `--userId`, so let's use the user ID in the error
						// message as opposed to the project ID.
						`the user with the ID "${userId}"`
					: `the project with the ID "${projectId}"`;

				return {
					success: false as const,
					message: `The credential with ID "${credential.id}" is already owned by ${currentOwner}. It can't be re-owned by ${newOwner}.`,
				};
			}
		}

		return {
			success: true as const,
			message: undefined,
		};
	}

	private async readCredentials(path: string, separate: boolean): Promise<ICredentialsEncrypted[]> {
		const cipher = Container.get(Cipher);

		if (process.platform === 'win32') {
			path = path.replace(/\\/g, '/');
		}

		let credentials: ICredentialsEncrypted[];

		if (separate) {
			const files = await glob('*.json', {
				cwd: path,
				absolute: true,
			});

			credentials = files.map((file) =>
				jsonParse<ICredentialsEncrypted>(fs.readFileSync(file, { encoding: 'utf8' })),
			);
		} else {
			const credentialsUnchecked = jsonParse<ICredentialsEncrypted[]>(
				fs.readFileSync(path, { encoding: 'utf8' }),
			);

			if (!Array.isArray(credentialsUnchecked)) {
				throw new UserError(
					'File does not seem to contain credentials. Make sure the credentials are contained in an array.',
				);
			}

			credentials = credentialsUnchecked;
		}

		return credentials.map((credential) => {
			if (typeof credential.data === 'object') {
				// plain data / decrypted input. Should be encrypted first.
				credential.data = cipher.encrypt(credential.data);
			}

			return credential;
		});
	}

	private async getCredentialOwner(credentialsId: string) {
		const sharedCredential = await this.transactionManager.findOne(SharedCredentials, {
			where: { credentialsId, role: 'credential:owner' },
			relations: { project: true },
		});

		if (sharedCredential && sharedCredential.project.type === 'personal') {
			const user = await this.transactionManager.findOneByOrFail(User, {
				projectRelations: {
					role: { slug: PROJECT_OWNER_ROLE_SLUG },
					projectId: sharedCredential.projectId,
				},
			});

			return { user, project: sharedCredential.project };
		}

		return {};
	}

	private async credentialExists(credentialId: string) {
		return await this.transactionManager.existsBy(CredentialsEntity, { id: credentialId });
	}

	private async getProject(userId?: string, projectId?: string) {
		if (projectId) {
			return await this.transactionManager.findOneByOrFail(Project, { id: projectId });
		}

		if (!userId) {
			const owner = await this.transactionManager.findOneBy(User, {
				role: {
					slug: GLOBAL_OWNER_ROLE.slug,
				},
			});
			if (!owner) {
				throw new UserError(`Failed to find owner. ${UM_FIX_INSTRUCTION}`);
			}
			userId = owner.id;
		}

		return await Container.get(ProjectRepository).getPersonalProjectForUserOrFail(
			userId,
			this.transactionManager,
		);
	}
}
