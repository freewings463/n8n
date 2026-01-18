"""
MIGRATION-META:
  source_path: packages/core/src/utils/signature-helpers.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/utils 的工具。导入/依赖:外部:无；内部:无；本地:无。导出:generateUrlSignature、prepareUrlForSigning。关键函数/方法:generateUrlSignature、prepareUrlForSigning。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Core utility helpers -> application/services/utils
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/utils/signature-helpers.ts -> services/n8n/application/core/services/utils/signature_helpers.py

import crypto from 'crypto';

/**
 * Generate signature token from url and secret
 */
export function generateUrlSignature(url: string, secret: string) {
	const token = crypto.createHmac('sha256', secret).update(url).digest('hex');
	return token;
}

/**
 * Prepare url for signing
 */
export function prepareUrlForSigning(url: URL) {
	return `${url.host}${url.pathname}${url.search}`;
}
