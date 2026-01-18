"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Shopify/OrderInterface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Shopify 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:ILineItem、IDiscountCode、IAddress、IOrder。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Shopify/OrderInterface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Shopify/OrderInterface.py

export interface ILineItem {
	id?: number;
	product_id?: number;
	variant_id?: number;
	title?: string;
	price?: string;
	grams?: string;
	quantity?: number;
}

export interface IDiscountCode {
	code?: string;
	amount?: string;
	type?: string;
}

export interface IAddress {
	first_name?: string;
	last_name?: string;
	company?: string;
	address1?: string;
	address2?: string;
	city?: string;
	province?: string;
	country?: string;
	phone?: string;
	zip?: string;
}

export interface IOrder {
	billing_address?: IAddress;
	discount_codes?: IDiscountCode[];
	email?: string;
	fulfillment_status?: string;
	inventory_behaviour?: string;
	line_items?: ILineItem[];
	location_id?: number;
	note?: string;
	send_fulfillment_receipt?: boolean;
	send_receipt?: boolean;
	shipping_address?: IAddress;
	source_name?: string;
	tags?: string;
	test?: boolean;
}
