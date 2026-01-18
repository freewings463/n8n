"""
MIGRATION-META:
  source_path: packages/@n8n/decorators/src/command/command-metadata.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/decorators/src/command 的模块。导入/依赖:外部:无；内部:@n8n/di；本地:./types。导出:CommandMetadata。关键函数/方法:register、get、getEntries。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/decorators/src/command/command-metadata.ts -> services/n8n/application/n8n-decorators/services/command/command_metadata.py

import { Service } from '@n8n/di';

import type { CommandEntry } from './types';

@Service()
export class CommandMetadata {
	private readonly commands: Map<string, CommandEntry> = new Map();

	register(name: string, entry: CommandEntry) {
		this.commands.set(name, entry);
	}

	get(name: string) {
		return this.commands.get(name);
	}

	getEntries() {
		return [...this.commands.entries()];
	}
}
