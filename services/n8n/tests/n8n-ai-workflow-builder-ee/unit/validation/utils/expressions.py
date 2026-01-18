"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/validation/utils/expressions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/validation/utils 的工作流工具。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:containsExpression、nodeParametersContainExpression。关键函数/方法:containsExpression、nodeParametersContainExpression。用于提供工作流通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/validation/utils/expressions.ts -> services/n8n/tests/n8n-ai-workflow-builder-ee/unit/validation/utils/expressions.py

import type { INodeParameters } from 'n8n-workflow';
import { isExpression } from 'n8n-workflow';

export function containsExpression(value: unknown): boolean {
	if (!isExpression(value)) {
		return false;
	}

	return /\{\{.*(\$\(.*?\))|(\$\w+).*}}/.test(value);
}

export function nodeParametersContainExpression(parameters: INodeParameters): boolean {
	for (const value of Object.values(parameters)) {
		if (containsExpression(value)) {
			return true;
		}

		if (value && typeof value === 'object' && !Array.isArray(value)) {
			if (nodeParametersContainExpression(value as INodeParameters)) {
				return true;
			}
		}

		if (Array.isArray(value)) {
			for (const item of value) {
				if (containsExpression(item)) {
					return true;
				}

				if (item && typeof item === 'object') {
					if (nodeParametersContainExpression(item as INodeParameters)) {
						return true;
					}
				}
			}
		}
	}

	return false;
}
