"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Copper/utils/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Copper/utils 的工具。导入/依赖:外部:无；内部:无；本地:无。导出:EmailFixedCollection、EmailsFixedCollection、PhoneNumbersFixedCollection、AddressFixedCollection。关键函数/方法:无。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Copper/utils/types.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Copper/utils/types.py

export type EmailFixedCollection = {
	email?: {
		emailFields: Array<{ email: string; category: string }>;
	};
};

export type EmailsFixedCollection = {
	emails?: {
		emailFields: Array<{ email: string; category: string }>;
	};
};

export type PhoneNumbersFixedCollection = {
	phone_numbers?: {
		phoneFields: object;
	};
};

export type AddressFixedCollection = {
	address?: {
		addressFields: object;
	};
};
