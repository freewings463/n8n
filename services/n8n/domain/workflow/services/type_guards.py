"""
MIGRATION-META:
  source_path: packages/workflow/src/type-guards.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src 的工作流模块。导入/依赖:外部:无；内部:无；本地:无。导出:isResourceLocatorValue、isINodeProperties、isINodePropertyOptions、isINodePropertyCollection、isINodePropertiesList、isINodePropertyOptionsList、isINodePropertyCollectionList、isValidResourceLocatorParameterValue 等4项。关键函数/方法:isResourceLocatorValue、isINodeProperties、isINodePropertyOptions、isINodePropertyCollection 等8项。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package workflow treated as domain model & rules
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/type-guards.ts -> services/n8n/domain/workflow/services/type_guards.py

import {
	type INodeProperties,
	type INodePropertyOptions,
	type INodePropertyCollection,
	type INodeParameterResourceLocator,
	type ResourceMapperValue,
	type FilterValue,
	type NodeConnectionType,
	nodeConnectionTypes,
	type IBinaryData,
} from './interfaces';

export function isResourceLocatorValue(value: unknown): value is INodeParameterResourceLocator {
	return Boolean(
		typeof value === 'object' && value && 'mode' in value && 'value' in value && '__rl' in value,
	);
}

export const isINodeProperties = (
	item: INodePropertyOptions | INodeProperties | INodePropertyCollection,
): item is INodeProperties => 'name' in item && 'type' in item && !('value' in item);

export const isINodePropertyOptions = (
	item: INodePropertyOptions | INodeProperties | INodePropertyCollection,
): item is INodePropertyOptions => 'value' in item && 'name' in item && !('displayName' in item);

export const isINodePropertyCollection = (
	item: INodePropertyOptions | INodeProperties | INodePropertyCollection,
): item is INodePropertyCollection => 'values' in item && 'name' in item && 'displayName' in item;

export const isINodePropertiesList = (
	items: INodeProperties['options'],
): items is INodeProperties[] => Array.isArray(items) && items.every(isINodeProperties);

export const isINodePropertyOptionsList = (
	items: INodeProperties['options'],
): items is INodePropertyOptions[] => Array.isArray(items) && items.every(isINodePropertyOptions);

export const isINodePropertyCollectionList = (
	items: INodeProperties['options'],
): items is INodePropertyCollection[] => {
	return Array.isArray(items) && items.every(isINodePropertyCollection);
};

export const isValidResourceLocatorParameterValue = (
	value: INodeParameterResourceLocator,
): boolean => {
	if (typeof value === 'object') {
		if (typeof value.value === 'number') {
			return true; // Accept all numbers
		}
		return !!value.value;
	} else {
		return !!value;
	}
};

export const isResourceMapperValue = (value: unknown): value is ResourceMapperValue => {
	return (
		typeof value === 'object' &&
		value !== null &&
		'mappingMode' in value &&
		'schema' in value &&
		'value' in value
	);
};

export const isFilterValue = (value: unknown): value is FilterValue => {
	return (
		typeof value === 'object' && value !== null && 'conditions' in value && 'combinator' in value
	);
};

export const isNodeConnectionType = (value: unknown): value is NodeConnectionType => {
	return nodeConnectionTypes.includes(value as NodeConnectionType);
};

export const isBinaryValue = (value: unknown): value is IBinaryData => {
	return (
		typeof value === 'object' &&
		value !== null &&
		'mimeType' in value &&
		('data' in value || 'id' in value)
	);
};
