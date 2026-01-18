"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/schemas/external-secrets.schema.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/schemas 的模块。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:ExternalSecretsProviderSecret、ExternalSecretsProviderData、ExternalSecretsProviderProperty、ExternalSecretsProviderState、ExternalSecretsProvider。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/schemas/external-secrets.schema.ts -> services/n8n/presentation/n8n-api-types/dto/schemas/external_secrets_schema.py

import type { NodeParameterValueType, INodeProperties } from 'n8n-workflow';

export interface ExternalSecretsProviderSecret {
	key: string;
}

export type ExternalSecretsProviderData = Record<string, NodeParameterValueType>;

export type ExternalSecretsProviderProperty = INodeProperties;

export type ExternalSecretsProviderState = 'connected' | 'tested' | 'initializing' | 'error';

export interface ExternalSecretsProvider {
	icon: string;
	name: string;
	displayName: string;
	connected: boolean;
	connectedAt: string | false;
	state: ExternalSecretsProviderState;
	data?: ExternalSecretsProviderData;
	properties?: ExternalSecretsProviderProperty[];
}
