"""
MIGRATION-META:
  source_path: packages/@n8n/utils/vite.config.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/utils 的工具。导入/依赖:外部:无；内部:@n8n/vitest-config/frontend；本地:无。导出:无。关键函数/方法:无。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Generic shared utilities -> application/services/utils
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/utils/vite.config.ts -> services/n8n/application/n8n-utils/services/utils/vite_config.py

import { vitestConfig } from '@n8n/vitest-config/frontend';

export default vitestConfig;
