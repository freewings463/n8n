"""
MIGRATION-META:
  source_path: packages/node-dev/commands/new.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/node-dev/commands 的模块。导入/依赖:外部:@oclif/core、change-case、fs/promises、inquirer；内部:无；本地:../src。导出:New。关键函数/方法:run。用于承载该模块实现细节，并通过导出对外提供能力。注释目标:eslint-disable @typescript-eslint/no-unsafe-argument。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected runtime IO/external interaction -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/node-dev/commands/new.ts -> services/n8n/infrastructure/node-dev/container/commands/new.py

/* eslint-disable @typescript-eslint/no-unsafe-argument */

/* eslint-disable @typescript-eslint/no-unsafe-call */
/* eslint-disable @typescript-eslint/no-unsafe-assignment */
import { Command } from '@oclif/core';
import * as changeCase from 'change-case';
import { access } from 'fs/promises';
import * as inquirer from 'inquirer';
import { join } from 'path';

import { createTemplate } from '../src';

export class New extends Command {
	static description = 'Create new credentials/node';

	static examples = ['$ n8n-node-dev new'];

	async run() {
		try {
			this.log('\nCreate new credentials/node');
			this.log('=========================');

			// Ask for the type of not to be created
			const typeQuestion: inquirer.QuestionCollection = {
				name: 'type',
				type: 'list',
				default: 'Node',
				message: 'What do you want to create?',
				choices: ['Credentials', 'Node'],
			};

			const typeAnswers = await inquirer.prompt(typeQuestion);

			let sourceFolder = '';
			const sourceFileName = 'simple.ts';
			let defaultName = '';
			let getDescription = false;

			if (typeAnswers.type === 'Node') {
				// Create new node

				getDescription = true;

				const nodeTypeQuestion: inquirer.QuestionCollection = {
					name: 'nodeType',
					type: 'list',
					default: 'Execute',
					message: 'What kind of node do you want to create?',
					choices: ['Execute', 'Trigger', 'Webhook'],
				};

				const nodeTypeAnswers = await inquirer.prompt(nodeTypeQuestion);

				// Choose a the template-source-file depending on user input.
				sourceFolder = 'execute';
				defaultName = 'My Node';
				if (nodeTypeAnswers.nodeType === 'Trigger') {
					sourceFolder = 'trigger';
					defaultName = 'My Trigger';
				} else if (nodeTypeAnswers.nodeType === 'Webhook') {
					sourceFolder = 'webhook';
					defaultName = 'My Webhook';
				}
			} else {
				// Create new credentials

				sourceFolder = 'credentials';
				defaultName = 'My Service API';
			}

			// Ask additional questions to know with what values the
			// variables in the template file should be replaced with
			const additionalQuestions = [
				{
					name: 'name',
					type: 'input',
					default: defaultName,
					message: 'How should the node be called?',
				},
			];

			if (getDescription) {
				// Get also a node description
				additionalQuestions.push({
					name: 'description',
					type: 'input',
					default: 'Node converts input data to chocolate',
					message: 'What should the node description be?',
				});
			}

			const additionalAnswers = await inquirer.prompt(
				additionalQuestions as inquirer.QuestionCollection,
			);

			const nodeName = additionalAnswers.name;

			// Define the source file to be used and the location and name of the new
			// node file
			const destinationFilePath = join(
				process.cwd(),
				// eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
				`${changeCase.pascalCase(nodeName)}.${typeAnswers.type.toLowerCase()}.ts`,
			);

			const sourceFilePath = join(__dirname, '../../templates', sourceFolder, sourceFileName);

			// Check if node with the same name already exists in target folder
			// to not overwrite it by accident
			try {
				await access(destinationFilePath);

				// File does already exist. So ask if it should be overwritten.
				const overwriteQuestion: inquirer.QuestionCollection = [
					{
						name: 'overwrite',
						type: 'confirm',
						default: false,
						message: `The file "${destinationFilePath}" already exists and would be overwritten. Do you want to proceed and overwrite the file?`,
					},
				];

				const overwriteAnswers = await inquirer.prompt(overwriteQuestion);

				if (overwriteAnswers.overwrite === false) {
					this.log('\nNode creation got canceled!');
					return;
				}
			} catch (error) {
				// File does not exist. That is exactly what we want so go on.
			}

			// Make sure that the variables in the template file get formatted
			// in the correct way
			const replaceValues = {
				ClassNameReplace: changeCase.pascalCase(nodeName),
				DisplayNameReplace: changeCase.capitalCase(nodeName),
				N8nNameReplace: changeCase.camelCase(nodeName),
				NodeDescriptionReplace: additionalAnswers.description,
			};

			await createTemplate(sourceFilePath, destinationFilePath, replaceValues);

			this.log('\nExecution was successful:');
			this.log('====================================');

			this.log(`Node got created: ${destinationFilePath}`);
		} catch (error) {
			// eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
			this.log(`\nGOT ERROR: "${error.message}"`);
			this.log('====================================');
			// eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
			this.log(error.stack);
		}
	}
}
