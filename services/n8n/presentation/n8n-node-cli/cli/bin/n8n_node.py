"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/bin/n8n-node.mjs
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/node-cli/bin 的模块。导入/依赖:外部:@oclif/core；内部:无；本地:无。导出:无。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI package default -> presentation/cli
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/bin/n8n-node.mjs -> services/n8n/presentation/n8n-node-cli/cli/bin/n8n_node.py

#!/usr/bin/env node

import { execute } from '@oclif/core';

await execute({ dir: import.meta.url });
