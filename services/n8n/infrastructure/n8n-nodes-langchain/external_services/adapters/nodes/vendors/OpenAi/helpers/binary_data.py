"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/helpers/binary-data.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/OpenAi 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:getBinaryDataFile。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/helpers/binary-data.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/OpenAi/helpers/binary_data.py

import type { IBinaryData, IExecuteFunctions } from 'n8n-workflow';

/** Chunk size to use for streaming. 256Kb */
const CHUNK_SIZE = 256 * 1024;

/**
 * Gets the binary data file for the given item index and given property name.
 * Returns the file name, content type and the file content. Uses streaming
 * when possible.
 */
export async function getBinaryDataFile(
	ctx: IExecuteFunctions,
	itemIdx: number,
	binaryPropertyData: string | IBinaryData,
) {
	const binaryData = ctx.helpers.assertBinaryData(itemIdx, binaryPropertyData);

	const fileContent = binaryData.id
		? await ctx.helpers.getBinaryStream(binaryData.id, CHUNK_SIZE)
		: await ctx.helpers.getBinaryDataBuffer(itemIdx, binaryPropertyData);

	return {
		filename: binaryData.fileName,
		contentType: binaryData.mimeType,
		fileContent,
	};
}
