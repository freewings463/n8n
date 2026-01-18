"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Shopify/ProductInterface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Shopify 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:IImage、IPrice、IPresentmentPrices、IVariant、IProduct。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Shopify/ProductInterface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Shopify/ProductInterface.py

import type { IDataObject } from 'n8n-workflow';

export interface IImage {
	id?: string;
	product_id?: string;
	position?: number;
	created_at?: string;
	updated_at?: string;
	width?: number;
	height?: number;
	src?: string;
	variant_ids?: number[];
}

export interface IPrice {
	currency_code?: string;
	amount?: string;
}

export interface IPresentmentPrices {
	price?: IPrice;
	compare_at_price?: IPrice;
}

export interface IVariant {
	barcode?: string;
	compare_at_price?: string;
	created_at?: string;
	fulfillment_service?: string;
	grams?: number;
	id?: number;
	image_id?: number;
	inventory_item_id?: number;
	inventory_management?: string;
	inventory_policy?: string;
	option1?: string;
	option2?: string;
	option3?: string;
	presentment_prices?: IPresentmentPrices[];
	price?: string;
	product_id?: number;
	sku?: string;
	taxable?: boolean;
	tax_code?: string;
	title?: string;
	updated_at?: string;
	weight?: number;
	weight_unit?: string;
}

export interface IProduct {
	body_html?: string;
	handle?: string;
	images?: IImage[];
	options?: IDataObject[];
	product_type?: string;
	published_at?: string;
	published_scope?: string;
	tags?: string;
	template_suffix?: string;
	title?: string;
	variants?: IVariant[];
	vendor?: string;
}
