"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/InvoiceNinja/QuoteInterface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/InvoiceNinja 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:IItem、IQuote。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/InvoiceNinja/QuoteInterface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/InvoiceNinja/QuoteInterface.py

export interface IItem {
	cost?: number;
	notes?: string;
	product_key?: string;
	qty?: number;
	quantity?: number;
	tax_rate1?: number;
	tax_rate2?: number;
	tax_name1?: string;
	tax_name2?: string;
}

export interface IQuote {
	auto_bill?: boolean;
	client_id?: number;
	custom_value1?: number;
	custom_value2?: number;
	email_invoice?: boolean;
	discount?: number;
	due_date?: string;
	email?: string;
	invoice_date?: string;
	invoice_items?: IItem[];
	line_items?: IItem[];
	invoice_number?: string;
	// eslint-disable-next-line id-denylist
	number?: string;
	invoice_status_id?: number;
	is_amount_discount?: boolean;
	is_quote?: boolean;
	paid?: number;
	partial?: number;
	partial_due_date?: string;
	po_number?: string;
	private_notes?: string;
	public_notes?: string;
	tax_name1?: string;
	tax_name2?: string;
	tax_rate1?: number;
	tax_rate2?: number;
}
