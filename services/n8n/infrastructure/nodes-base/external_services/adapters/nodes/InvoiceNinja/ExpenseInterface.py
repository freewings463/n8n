"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/InvoiceNinja/ExpenseInterface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/InvoiceNinja 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:IExpense。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/InvoiceNinja/ExpenseInterface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/InvoiceNinja/ExpenseInterface.py

export interface IExpense {
	amount?: number;
	client_id?: number;
	custom_value1?: string;
	custom_value2?: string;
	expense_category_id?: number;
	expense_date?: string;
	payment_date?: string;
	payment_type_id?: number;
	private_notes?: string;
	public_notes?: string;
	should_be_invoiced?: boolean;
	tax_name1?: string;
	tax_name2?: string;
	tax_rate1?: number;
	tax_rate2?: number;
	transaction_reference?: string;
	vendor_id?: number;
}
