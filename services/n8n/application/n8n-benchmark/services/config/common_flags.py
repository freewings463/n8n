"""
MIGRATION-META:
  source_path: packages/@n8n/benchmark/src/config/common-flags.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/benchmark/src/config 的配置。导入/依赖:外部:@oclif/core；内部:无；本地:无。导出:testScenariosPath。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Benchmark orchestration logic -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/benchmark/src/config/common-flags.ts -> services/n8n/application/n8n-benchmark/services/config/common_flags.py

import { Flags } from '@oclif/core';

export const testScenariosPath = Flags.string({
	description: 'The path to the scenarios',
	default: 'scenarios',
});
