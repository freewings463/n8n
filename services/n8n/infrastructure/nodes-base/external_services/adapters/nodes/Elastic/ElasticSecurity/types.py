"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Elastic/ElasticSecurity/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Elastic/ElasticSecurity 的类型。导入/依赖:外部:无；内部:无；本地:无。导出:ElasticSecurityApiCredentials、ConnectorType、Connector、ConnectorCreatePayload。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Elastic/ElasticSecurity/types.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Elastic/ElasticSecurity/types.py

export type ElasticSecurityApiCredentials = {
	username?: string;
	password?: string;
	apiKey?: string;
	baseUrl: string;
};

export type ConnectorType = '.jira' | '.servicenow' | '.resilient';

export type Connector = {
	id: string;
	name: string;
	connector_type_id: ConnectorType;
};

export type ConnectorCreatePayload =
	| ServiceNowConnectorCreatePayload
	| JiraConnectorCreatePayload
	| IbmResilientConnectorCreatePayload;

type ServiceNowConnectorCreatePayload = {
	connector_type_id: '.servicenow';
	name: string;
	secrets?: {
		username: string;
		password: string;
	};
	config?: {
		apiUrl: string;
	};
};

type JiraConnectorCreatePayload = {
	connector_type_id: '.jira';
	name: string;
	secrets?: {
		email: string;
		apiToken: string;
	};
	config?: {
		apiUrl: string;
		projectKey: string;
	};
};

type IbmResilientConnectorCreatePayload = {
	connector_type_id: '.resilient';
	name: string;
	secrets?: {
		apiKeyId: string;
		apiKeySecret: string;
	};
	config?: {
		apiUrl: string;
		orgId: string;
	};
};
