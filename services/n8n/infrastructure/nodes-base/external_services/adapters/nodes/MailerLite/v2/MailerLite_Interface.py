"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/MailerLite/v2/MailerLite.Interface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/MailerLite/v2 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:CustomField、SubscriberFields、Subscriber。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/MailerLite/v2/MailerLite.Interface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/MailerLite/v2/MailerLite_Interface.py

export interface CustomField {
	name: string;
	key: string;
}

export interface SubscriberFields {
	city: string | null;
	company: string | null;
	country: string | null;
	last_name: string | null;
	name: string | null;
	phone: string | null;
	state: string | null;
	z_i_p: string | null;
}

export interface Subscriber {
	id: string;
	email: string;
	status: string;
	source: string;
	sent: number;
	opens_count: number;
	clicks_count: number;
	open_rate: number;
	click_rate: number;
	ip_address: string | null;
	subscribed_at: string;
	unsubscribed_at: string | null;
	created_at: string;
	updated_at: string;
	fields: SubscriberFields;
	opted_in_at: string | null;
	optin_ip: string | null;
}
