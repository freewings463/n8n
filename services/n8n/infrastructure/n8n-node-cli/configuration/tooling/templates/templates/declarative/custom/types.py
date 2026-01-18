"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/template/templates/declarative/custom/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/template/templates/declarative 的类型。导入/依赖:外部:无；内部:无；本地:无。导出:CustomTemplateConfig、CredentialType。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - node-cli templates -> infrastructure/configuration/tooling/templates
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/template/templates/declarative/custom/types.ts -> services/n8n/infrastructure/n8n-node-cli/configuration/tooling/templates/templates/declarative/custom/types.py

export type CustomTemplateConfig =
	| {
			credentialType: 'apiKey' | 'bearer' | 'basicAuth' | 'custom' | 'none';
			baseUrl: string;
	  }
	| { credentialType: 'oauth2'; baseUrl: string; flow: string };

export type CredentialType = CustomTemplateConfig['credentialType'];
