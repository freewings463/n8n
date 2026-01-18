"""
MIGRATION-META:
  source_path: packages/cli/src/utils/cors.util.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/utils 的工具。导入/依赖:外部:express；内部:无；本地:无。导出:applyCors。关键函数/方法:applyCors。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/utils/cors.util.ts -> services/n8n/presentation/cli/api/utils/cors_util.py

import type { Request, Response } from 'express';

export function applyCors(req: Request, res: Response) {
	if (res.getHeader('Access-Control-Allow-Origin')) {
		return;
	}

	const origin = req.headers.origin;

	if (!origin || origin === 'null') {
		res.setHeader('Access-Control-Allow-Origin', '*');
	} else {
		res.setHeader('Access-Control-Allow-Origin', origin);
	}

	res.setHeader('Access-Control-Allow-Methods', 'POST, GET, OPTIONS');
	res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
}
