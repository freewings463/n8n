"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Keap/EcommerceOrderInterface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Keap 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:IItem、IShippingAddress、IEcommerceOrder。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Keap/EcommerceOrderInterface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Keap/EcommerceOrderInterface.py

export interface IItem {
	description?: string;
	price?: number;
	product_id?: number;
	quantity?: number;
}

export interface IShippingAddress {
	company?: string;
	country_code?: string;
	first_name?: string;
	last_name?: string;
	line1?: string;
	line2?: string;
	locality?: string;
	middle_name?: string;
	postal_code?: string;
	region?: string;
	zip_code?: string;
	zip_four?: string;
}

export interface IEcommerceOrder {
	contact_id: number;
	lead_affiliate_id?: string;
	order_date: string;
	order_items?: IItem[];
	order_title: string;
	order_type?: string;
	promo_codes?: string[];
	sales_affiliate_id?: number;
	shipping_address?: IShippingAddress;
}
