"""
MIGRATION-META:
  source_path: packages/@n8n/extension-sdk/src/frontend/types.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/extension-sdk/src/frontend 的类型。导入/依赖:外部:vue-router、vue；内部:无；本地:无。导出:FrontendExtensionContext、FrontendExtensionSetupFn、FrontendExtension。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Extension SDK contracts/helpers -> presentation/dto
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/extension-sdk/src/frontend/types.ts -> services/n8n/presentation/n8n-extension-sdk/dto/extension_sdk/frontend/types.py

import type { RouteRecordRaw } from 'vue-router';
import type { App, Component } from 'vue';

export type FrontendExtensionContext = {
	app: App;
	defineRoutes: (routes: RouteRecordRaw[]) => void;
	registerComponent: (name: string, component: Component) => void;
};

export type FrontendExtensionSetupFn = (context: FrontendExtensionContext) => void;

export type FrontendExtension = {
	setup: FrontendExtensionSetupFn;
};
