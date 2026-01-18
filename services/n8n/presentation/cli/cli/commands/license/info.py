"""
MIGRATION-META:
  source_path: packages/cli/src/commands/license/info.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/commands/license 的模块。导入/依赖:外部:无；内部:@n8n/decorators、@n8n/di、@/license；本地:../base-command。导出:LicenseInfoCommand。关键函数/方法:run。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - CLI command -> presentation/cli/commands
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/commands/license/info.ts -> services/n8n/presentation/cli/cli/commands/license/info.py

import { Command } from '@n8n/decorators';
import { Container } from '@n8n/di';

import { License } from '@/license';

import { BaseCommand } from '../base-command';

@Command({
	name: 'license:info',
	description: 'Print license information',
})
export class LicenseInfoCommand extends BaseCommand {
	async run() {
		const license = Container.get(License);
		await license.init({ isCli: true });

		this.logger.info('Printing license information:\n' + license.getInfo());
	}

	async catch(error: Error) {
		this.logger.error('\nGOT ERROR');
		this.logger.info('====================================');
		this.logger.error(error.message);
	}
}
