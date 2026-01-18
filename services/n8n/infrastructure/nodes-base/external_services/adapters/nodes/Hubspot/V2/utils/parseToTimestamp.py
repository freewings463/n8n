"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Hubspot/V2/utils/parseToTimestamp.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Hubspot/V2 的工具。导入/依赖:外部:moment-timezone；内部:无；本地:无。导出:parseToTimestamp。关键函数/方法:parseToTimestamp。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Hubspot/V2/utils/parseToTimestamp.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Hubspot/V2/utils/parseToTimestamp.py

import moment from 'moment-timezone';

export function parseToTimestamp(dateString: unknown): number {
	if (typeof dateString !== 'string') {
		throw new Error('Invalid date string');
	}
	const timestamp = moment(dateString).valueOf();
	if (isNaN(timestamp)) {
		throw new Error('Invalid date string');
	}
	return timestamp;
}
