"""
MIGRATION-META:
  source_path: packages/extensions/insights/src/backend/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/extensions/src/backend 的Insights入口。导入/依赖:外部:无；内部:@n8n/extension-sdk/backend；本地:无。导出:无。关键函数/方法:setup。用于汇总导出并完成Insights模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Extensions package -> infrastructure/configuration/tooling/extensions
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/extensions/insights/src/backend/index.ts -> services/n8n/infrastructure/extensions/configuration/tooling/extensions/insights/src/backend/__init__.py

import { defineBackendExtension } from '@n8n/extension-sdk/backend';

export default defineBackendExtension({
	setup(n8n) {
		console.log(n8n);
	},
});
