"""
MIGRATION-META:
  source_path: packages/core/src/instance-settings/worker-missing-encryption-key.error.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/core/src/instance-settings 的错误。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:WorkerMissingEncryptionKey。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Instance settings wiring -> infrastructure/configuration
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/instance-settings/worker-missing-encryption-key.error.ts -> services/n8n/infrastructure/core/configuration/instance_settings/worker_missing_encryption_key_error.py

import { UserError } from 'n8n-workflow';

export class WorkerMissingEncryptionKey extends UserError {
	constructor() {
		super(
			[
				'Failed to start worker because of missing encryption key.',
				'Please set the `N8N_ENCRYPTION_KEY` env var when starting the worker.',
				'See: https://docs.n8n.io/hosting/configuration/configuration-examples/encryption-key/',
			].join(' '),
		);
	}
}
