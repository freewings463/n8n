"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/InvoiceNinja/PaymentInterface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/InvoiceNinja 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:IPayment、IInvoice。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/InvoiceNinja/PaymentInterface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/InvoiceNinja/PaymentInterface.py

export interface IPayment {
	invoice_id?: number;
	amount?: number;
	payment_type_id?: number;
	type_id?: number;
	transaction_reference?: string;
	private_notes?: string;
	client_id?: string;
	invoices?: IInvoice[];
}

export interface IInvoice {
	invoice_id: string;
	amount: number;
}
