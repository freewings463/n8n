"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Transform/Aggregate/utils.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Transform/Aggregate 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:addBinariesToItem。关键函数/方法:isBinaryUniqueSetup、addBinariesToItem。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Transform/Aggregate/utils.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Transform/Aggregate/utils.py

import type { IBinaryData, INodeExecutionData } from 'n8n-workflow';

type PartialBinaryData = Omit<IBinaryData, 'data'>;
const isBinaryUniqueSetup = () => {
	const binaries: PartialBinaryData[] = [];
	return (binary: IBinaryData) => {
		for (const existingBinary of binaries) {
			if (
				existingBinary.mimeType === binary.mimeType &&
				existingBinary.fileType === binary.fileType &&
				existingBinary.fileSize === binary.fileSize &&
				existingBinary.fileExtension === binary.fileExtension
			) {
				return false;
			}
		}

		binaries.push({
			mimeType: binary.mimeType,
			fileType: binary.fileType,
			fileSize: binary.fileSize,
			fileExtension: binary.fileExtension,
		});

		return true;
	};
};

export function addBinariesToItem(
	newItem: INodeExecutionData,
	items: INodeExecutionData[],
	uniqueOnly?: boolean,
) {
	const isBinaryUnique = uniqueOnly ? isBinaryUniqueSetup() : undefined;

	for (const item of items) {
		if (item.binary === undefined) continue;

		for (const key of Object.keys(item.binary)) {
			if (!newItem.binary) newItem.binary = {};
			let binaryKey = key;
			const binary = item.binary[key];

			if (isBinaryUnique && !isBinaryUnique(binary)) {
				continue;
			}

			// If the binary key already exists add a suffix to it
			let i = 1;
			while (newItem.binary[binaryKey] !== undefined) {
				binaryKey = `${key}_${i}`;
				i++;
			}

			newItem.binary[binaryKey] = binary;
		}
	}

	return newItem;
}
