"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/template/templates/shared/default/eslint.config.mjs
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/template/templates/shared 的配置。导入/依赖:外部:无；内部:@n8n/node-cli/eslint；本地:无。导出:无。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - node-cli templates -> infrastructure/configuration/tooling/templates
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/template/templates/shared/default/eslint.config.mjs -> services/n8n/infrastructure/n8n-node-cli/configuration/tooling/templates/templates/shared/default/eslint_config.py

import { config } from '@n8n/node-cli/eslint';

export default config;
