"""
MIGRATION-META:
  source_path: packages/@n8n/backend-common/src/cli-parser.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/backend-common/src 的模块。导入/依赖:外部:yargs-parser、zod；内部:@n8n/di；本地:./logging。导出:CliParser。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/backend-common/src/cli-parser.ts -> services/n8n/application/n8n-backend-common/services/cli_parser.py

import { Service } from '@n8n/di';
import argvParser from 'yargs-parser';
import type { z } from 'zod';

import { Logger } from './logging';

type CliInput<Flags extends z.ZodRawShape> = {
	argv: string[];
	flagsSchema?: z.ZodObject<Flags>;
	description?: string;
	examples?: string[];
};

type ParsedArgs<Flags = Record<string, unknown>> = {
	flags: Flags;
	args: string[];
};

@Service()
export class CliParser {
	constructor(private readonly logger: Logger) {}

	parse<Flags extends z.ZodRawShape>(
		input: CliInput<Flags>,
	): ParsedArgs<z.infer<z.ZodObject<Flags>>> {
		// eslint-disable-next-line id-denylist
		const { _: rest, ...rawFlags } = argvParser(input.argv, { string: ['id'] });

		let flags = {} as z.infer<z.ZodObject<Flags>>;
		if (input.flagsSchema) {
			for (const key in input.flagsSchema.shape) {
				const flagSchema = input.flagsSchema.shape[key];
				let schemaDef = flagSchema._def as z.ZodTypeDef & {
					typeName: string;
					innerType?: z.ZodType;
					_alias?: string;
				};

				if (schemaDef.typeName === 'ZodOptional' && schemaDef.innerType) {
					schemaDef = schemaDef.innerType._def as typeof schemaDef;
				}

				const alias = schemaDef._alias;
				if (alias?.length && !(key in rawFlags) && rawFlags[alias]) {
					rawFlags[key] = rawFlags[alias] as unknown;
				}
			}

			flags = input.flagsSchema.parse(rawFlags);
		}

		const args = rest.map(String).slice(2);

		this.logger.debug('Received CLI command', {
			execPath: rest[0],
			scriptPath: rest[1],
			args,
			flags,
		});

		return { flags, args };
	}
}
