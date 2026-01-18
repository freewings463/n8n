"""
MIGRATION-META:
  source_path: packages/@n8n/decorators/src/command/command.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/decorators/src/command 的模块。导入/依赖:外部:无；内部:@n8n/di；本地:./command-metadata、./types。导出:Command。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - DI/container wiring -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/decorators/src/command/command.ts -> services/n8n/infrastructure/n8n-decorators/container/src/command/command.py

import { Container, Service } from '@n8n/di';

import { CommandMetadata } from './command-metadata';
import type { CommandClass, CommandOptions } from './types';

export const Command =
	({ name, description, examples, flagsSchema }: CommandOptions): ClassDecorator =>
	(target) => {
		const commandClass = target as unknown as CommandClass;
		Container.get(CommandMetadata).register(name, {
			description,
			flagsSchema,
			class: commandClass,
			examples,
		});
		// eslint-disable-next-line @typescript-eslint/no-unsafe-return
		return Service()(target);
	};
