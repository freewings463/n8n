"""
MIGRATION-META:
  source_path: packages/nodes-base/utils/workflowInputsResourceMapping/constants.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/utils/workflowInputsResourceMapping 的工作流工具。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:INPUT_SOURCE、WORKFLOW_INPUTS、VALUES、JSON_EXAMPLE、PASSTHROUGH、TYPE_OPTIONS、FALLBACK_DEFAULT_VALUE。关键函数/方法:无。用于提供工作流通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Integration package defaulted to infrastructure/external_services
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/utils/workflowInputsResourceMapping/constants.ts -> services/n8n/infrastructure/nodes-base/external_services/utils/workflowInputsResourceMapping/constants.py

import type { FieldType } from 'n8n-workflow';

export const INPUT_SOURCE = 'inputSource';
export const WORKFLOW_INPUTS = 'workflowInputs';
export const VALUES = 'values';
export const JSON_EXAMPLE = 'jsonExample';
export const PASSTHROUGH = 'passthrough';
export const TYPE_OPTIONS: Array<{ name: string; value: FieldType | 'any' }> = [
	{
		name: 'Allow Any Type',
		value: 'any',
	},
	{
		name: 'String',
		value: 'string',
	},
	{
		name: 'Number',
		value: 'number',
	},
	{
		name: 'Boolean',
		value: 'boolean',
	},
	{
		name: 'Array',
		value: 'array',
	},
	{
		name: 'Object',
		value: 'object',
	},
	// Intentional omission of `dateTime`, `time`, `string-alphanumeric`, `form-fields`, `jwt` and `url`
];

export const FALLBACK_DEFAULT_VALUE = null;
