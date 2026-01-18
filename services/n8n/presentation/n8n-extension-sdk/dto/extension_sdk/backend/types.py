"""
MIGRATION-META:
  source_path: packages/@n8n/extension-sdk/src/backend/types.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/extension-sdk/src/backend 的类型。导入/依赖:外部:无；内部:无；本地:无。导出:BackendExtensionContext、BackendExtensionSetupFn、BackendExtension。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Extension SDK contracts/helpers -> presentation/dto
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/extension-sdk/src/backend/types.ts -> services/n8n/presentation/n8n-extension-sdk/dto/extension_sdk/backend/types.py

export type BackendExtensionContext = {
	example?: string;
};

export type BackendExtensionSetupFn = (context: BackendExtension) => void;

export type BackendExtension = {
	setup: BackendExtensionSetupFn;
};
