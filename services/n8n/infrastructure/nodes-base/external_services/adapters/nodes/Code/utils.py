"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Code/utils.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Code 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:isObject、standardizeOutput、addPostExecutionWarning。关键函数/方法:isObject、isTraversable、standardizeOutput、standardizeOutputRecursive、addPostExecutionWarning。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Code/utils.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Code/utils.py

import type { INodeExecutionData, IDataObject, IExecuteFunctions } from 'n8n-workflow';

export function isObject(maybe: unknown): maybe is { [key: string]: unknown } {
	return (
		typeof maybe === 'object' && maybe !== null && !Array.isArray(maybe) && !(maybe instanceof Date)
	);
}

function isTraversable(maybe: unknown): maybe is IDataObject {
	return isObject(maybe) && typeof maybe.toJSON !== 'function' && Object.keys(maybe).length > 0;
}

/**
 * Stringify any non-standard JS objects (e.g. `Date`, `RegExp`) inside output items at any depth.
 */
export function standardizeOutput(output: IDataObject) {
	function standardizeOutputRecursive(obj: IDataObject, knownObjects = new WeakSet()): IDataObject {
		for (const [key, value] of Object.entries(obj)) {
			if (!isTraversable(value)) continue;

			if (typeof value === 'object' && value !== null) {
				if (knownObjects.has(value)) {
					// Found circular reference
					continue;
				}
				knownObjects.add(value);
			}

			obj[key] =
				value.constructor.name !== 'Object'
					? JSON.stringify(value) // Date, RegExp, etc.
					: standardizeOutputRecursive(value, knownObjects);
		}
		return obj;
	}
	standardizeOutputRecursive(output);
	return output;
}

export const addPostExecutionWarning = (
	context: IExecuteFunctions,
	returnData: INodeExecutionData[],
	inputItemsLength: number,
): void => {
	if (
		returnData.length !== inputItemsLength ||
		returnData.some((item) => item.pairedItem === undefined)
	) {
		context.addExecutionHints({
			message:
				'To make sure expressions after this node work, return the input items that produced each output item. <a target="_blank" href="https://docs.n8n.io/data/data-mapping/data-item-linking/item-linking-code-node/">More info</a>',
			location: 'outputPane',
		});
	}
};
