"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/InvoiceNinja/ClientInterface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/InvoiceNinja 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:IContact、IClient。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/InvoiceNinja/ClientInterface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/InvoiceNinja/ClientInterface.py

export interface IContact {
	first_name?: string;
	last_name?: string;
	email?: string;
	phone?: string;
}

export interface IClient {
	contacts?: IContact[];
	name?: string;
	address1?: string;
	address2?: string;
	city?: string;
	state?: string;
	postal_code?: string;
	country_id?: number;
	shipping_address1?: string;
	shipping_address2?: string;
	shipping_city?: string;
	shipping_state?: string;
	shipping_postal_code?: string;
	shipping_country_id?: number;
	work_phone?: string;
	private_notes?: string;
	website?: string;
	vat_number?: string;
	id_number?: string;
}
