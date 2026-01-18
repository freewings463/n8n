"""
MIGRATION-META:
  source_path: packages/cli/src/errors/node-crashed.error.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/errors 的错误。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:NodeCrashedError。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/errors/node-crashed.error.ts -> services/n8n/application/cli/services/errors/node_crashed_error.py

import type { INode } from 'n8n-workflow';
import { NodeOperationError } from 'n8n-workflow';

export class NodeCrashedError extends NodeOperationError {
	constructor(node: INode) {
		super(node, 'Node crashed, possible out-of-memory issue', {
			message: 'Execution stopped at this node',
			description:
				"n8n may have run out of memory while running this execution. More context and tips on how to avoid this <a href='https://docs.n8n.io/hosting/scaling/memory-errors/' target='_blank'>in the docs</a>",
		});
	}
}
