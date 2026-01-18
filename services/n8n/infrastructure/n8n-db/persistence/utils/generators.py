"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/utils/generators.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/utils 的工具。导入/依赖:外部:nanoid；内部:@n8n/constants、n8n-workflow；本地:无。导出:generateNanoId、generateHostInstanceId。关键函数/方法:generateNanoId、generateHostInstanceId。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package @n8n/db defaulted to persistence infrastructure
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/utils/generators.ts -> services/n8n/infrastructure/n8n-db/persistence/utils/generators.py

import type { InstanceType } from '@n8n/constants';
import { ALPHABET } from 'n8n-workflow';
import { customAlphabet } from 'nanoid';

const nanoid = customAlphabet(ALPHABET, 16);

export function generateNanoId() {
	return nanoid();
}

export function generateHostInstanceId(instanceType: InstanceType) {
	return `${instanceType}-${nanoid()}`;
}
