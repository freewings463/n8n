"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Transform/utils/utils.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Transform/utils 的工具。导入/依赖:外部:无；内部:@n8n/errors；本地:无。导出:prepareFieldsArray。关键函数/方法:prepareFieldsArray。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Transform/utils/utils.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Transform/utils/utils.py

import { ApplicationError } from '@n8n/errors';

export const prepareFieldsArray = (fields: string | string[], fieldName = 'Fields') => {
	if (typeof fields === 'string') {
		return fields
			.split(',')
			.map((entry) => entry.trim())
			.filter((entry) => entry !== '');
	}
	if (Array.isArray(fields)) {
		return fields;
	}
	throw new ApplicationError(
		`The \'${fieldName}\' parameter must be a string of fields separated by commas or an array of strings.`,
		{ level: 'warning' },
	);
};
