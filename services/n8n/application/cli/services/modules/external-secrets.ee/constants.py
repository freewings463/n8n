"""
MIGRATION-META:
  source_path: packages/cli/src/modules/external-secrets.ee/constants.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/external-secrets.ee 的模块。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:EXTERNAL_SECRETS_DB_KEY、EXTERNAL_SECRETS_INITIAL_BACKOFF、EXTERNAL_SECRETS_MAX_BACKOFF、EXTERNAL_SECRETS_NAME_REGEX、DOCS_HELP_NOTICE。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/external-secrets.ee/constants.ts -> services/n8n/application/cli/services/modules/external-secrets.ee/constants.py

import type { INodeProperties } from 'n8n-workflow';

export const EXTERNAL_SECRETS_DB_KEY = 'feature.externalSecrets';
export const EXTERNAL_SECRETS_INITIAL_BACKOFF = 10 * 1000;
export const EXTERNAL_SECRETS_MAX_BACKOFF = 5 * 60 * 1000;

export const EXTERNAL_SECRETS_NAME_REGEX = /^[a-zA-Z0-9\-\_\/]+$/;

export const DOCS_HELP_NOTICE: INodeProperties = {
	displayName:
		'Need help filling out these fields? <a href="https://docs.n8n.io/external-secrets/#connect-n8n-to-your-secrets-store" target="_blank">Open docs</a>',
	name: 'notice',
	type: 'notice',
	default: '',
	noDataExpression: true,
};
