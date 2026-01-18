"""
MIGRATION-META:
  source_path: packages/cli/src/modules/breaking-changes/rules/v2/binary-data-storage.rule.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/breaking-changes/rules 的模块。导入/依赖:外部:无；内部:@n8n/config、@n8n/di、n8n-core；本地:../../types。导出:BinaryDataStorageRule。关键函数/方法:getMetadata、detect。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/breaking-changes/rules/v2/binary-data-storage.rule.ts -> services/n8n/application/cli/services/breaking-changes/rules/v2/binary_data_storage_rule.py

import { ExecutionsConfig } from '@n8n/config';
import { Service } from '@n8n/di';
import { BinaryDataConfig } from 'n8n-core';

import type {
	BreakingChangeRuleMetadata,
	IBreakingChangeInstanceRule,
	InstanceDetectionReport,
} from '../../types';
import { BreakingChangeCategory } from '../../types';

@Service()
export class BinaryDataStorageRule implements IBreakingChangeInstanceRule {
	constructor(
		private readonly config: BinaryDataConfig,
		private readonly executionsConfig: ExecutionsConfig,
	) {}

	id: string = 'binary-data-storage-v2';

	getMetadata(): BreakingChangeRuleMetadata {
		return {
			version: 'v2',
			title: 'Binary data in-memory mode is removed',
			description:
				'Binary files are now stored on disk (default in regular mode) or in database (default in queue mode) instead of in memory',
			category: BreakingChangeCategory.infrastructure,
			severity: 'low',
			documentationUrl:
				'https://docs.n8n.io/2-0-breaking-changes/#remove-in-memory-binary-data-mode',
		};
	}

	async detect(): Promise<InstanceDetectionReport> {
		if (this.config.mode !== 'default') {
			return {
				isAffected: false,
				instanceIssues: [],
				recommendations: [],
			};
		}

		const isRegularMode = this.executionsConfig.mode === 'regular';

		const result: InstanceDetectionReport = {
			isAffected: true,
			instanceIssues: [
				{
					title: 'Binary data storage mode changed',
					description: isRegularMode
						? `Binary files are now stored in ${this.config.localStoragePath} directory by default (for regular mode) instead of in memory.`
						: 'Binary files are now stored in the database by default (for queue mode) instead of in memory.',
					level: 'info',
				},
			],
			recommendations: isRegularMode
				? [
						{
							action: 'Ensure adequate disk space',
							description: `Verify sufficient disk space is available for binary file storage in the ${this.config.localStoragePath} directory`,
						},
						{
							action: 'Configure persistent storage',
							description:
								'If using containers, ensure the binary data directory is mounted on a persistent volume',
						},
						{
							action: 'Include in backups',
							description: 'Add the binary data folder to your backup procedures',
						},
					]
				: [],
		};

		return result;
	}
}
