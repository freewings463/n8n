"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/PayPal/PaymentInteface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/PayPal 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:RecipientTypes、RecipientType、RecipientWallets、RecipientWallet、IAmount、ISenderBatchHeader、IItem、IPaymentBatch。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/PayPal/PaymentInteface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/PayPal/PaymentInteface.py

export const RecipientTypes = {
	email: 'EMAIL',
	phone: 'PHONE',
	paypalId: 'PAYPAL_ID',
} as const;

export type RecipientType = (typeof RecipientTypes)[keyof typeof RecipientTypes];

export const RecipientWallets = {
	paypal: 'PAYPAL',
	venmo: 'VENMO',
} as const;

export type RecipientWallet = (typeof RecipientWallets)[keyof typeof RecipientWallets];

export interface IAmount {
	currency?: string;
	value?: number;
}

export interface ISenderBatchHeader {
	sender_batch_id?: string;
	email_subject?: string;
	email_message?: string;
	note?: string;
}

export interface IItem {
	recipient_type?: RecipientType;
	amount?: IAmount;
	note?: string;
	receiver?: string;
	sender_item_id?: string;
	recipient_wallet?: RecipientWallet;
}

export interface IPaymentBatch {
	sender_batch_header?: ISenderBatchHeader;
	items?: IItem[];
}
