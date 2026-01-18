"""
MIGRATION-META:
  source_path: packages/extensions/insights/stylelint.config.mjs
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/extensions/insights 的Insights配置。导入/依赖:外部:无；内部:@n8n/stylelint-config/base；本地:无。导出:无。关键函数/方法:无。用于集中定义Insights配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Extensions package -> infrastructure/configuration/tooling/extensions
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/extensions/insights/stylelint.config.mjs -> services/n8n/infrastructure/extensions/configuration/tooling/extensions/insights/stylelint_config.py

import { baseConfig } from '@n8n/stylelint-config/base';

export default baseConfig;
