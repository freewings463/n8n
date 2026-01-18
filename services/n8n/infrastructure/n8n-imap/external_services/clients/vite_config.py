"""
MIGRATION-META:
  source_path: packages/@n8n/imap/vite.config.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/imap 的配置。导入/依赖:外部:无；内部:@n8n/vitest-config/node；本地:无。导出:无。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/imap treated as external service client library
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/imap/vite.config.ts -> services/n8n/infrastructure/n8n-imap/external_services/clients/vite_config.py

import { vitestConfig } from '@n8n/vitest-config/node';

export default vitestConfig;
