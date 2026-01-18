"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/WooCommerce/OrderInterface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/WooCommerce 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:IAddress、ILineItem、IShoppingLine、IFeeLine、ICouponLine、IOrder。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/WooCommerce/OrderInterface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/WooCommerce/OrderInterface.py

import type { IDataObject } from 'n8n-workflow';

export interface IAddress {
	first_name?: string;
	last_name?: string;
	company?: string;
	address_1?: string;
	address_2?: string;
	city?: string;
	state?: string;
	postcode?: string;
	country?: string;
	email?: string;
	phone?: string;
}

export interface ILineItem {
	name?: string;
	product_id?: number;
	variation_id?: number;
	quantity?: string;
	tax_class?: string;
	subtotal?: string;
	total?: string;
	meta_data?: IDataObject;
}

export interface IShoppingLine {
	method_title?: string;
	method_id?: number;
	total?: string;
	meta_data?: IDataObject;
}

export interface IFeeLine {
	name?: string;
	tax_class?: string;
	tax_status?: string;
	total?: string;
	meta_data?: IDataObject;
}

export interface ICouponLine {
	code?: string;
	meta_data?: IDataObject;
}

export interface IOrder {
	[index: string]: any;
	billing?: IAddress;
	coupon_lines?: ICouponLine[];
	currency?: string;
	customer_id?: number;
	customer_note?: string;
	fee_lines?: IFeeLine[];
	line_items?: ILineItem[];
	meta_data?: IDataObject[];
	parent_id?: number;
	payment_method?: string;
	payment_method_title?: string;
	set_paid?: boolean;
	shipping?: IAddress;
	shipping_lines?: IShoppingLine[];
	status?: string;
	transaction_id?: string;
}
