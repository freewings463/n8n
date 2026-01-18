"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/SqlAgent/other/handlers/sqlite.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/agents/Agent 的节点。导入/依赖:外部:sqlite3、temp；内部:@n8n/typeorm、n8n-workflow；本地:无。导出:无。关键函数/方法:getSqliteDataSource。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected runtime IO/external interaction -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/SqlAgent/other/handlers/sqlite.ts -> services/n8n/infrastructure/n8n-nodes-langchain/container/nodes/agents/Agent/agents/SqlAgent/other/handlers/sqlite.py

import { DataSource } from '@n8n/typeorm';
import * as fs from 'fs';
import type { IExecuteFunctions, INodeExecutionData } from 'n8n-workflow';
import { BINARY_ENCODING, NodeOperationError } from 'n8n-workflow';
import * as sqlite3 from 'sqlite3';
import * as temp from 'temp';

export async function getSqliteDataSource(
	this: IExecuteFunctions,
	binary: INodeExecutionData['binary'],
	binaryPropertyName = 'data',
): Promise<DataSource> {
	const binaryData = binary?.[binaryPropertyName];

	if (!binaryData) {
		throw new NodeOperationError(this.getNode(), 'No binary data received.');
	}

	let fileBase64;
	if (binaryData.id) {
		const chunkSize = 256 * 1024;
		const stream = await this.helpers.getBinaryStream(binaryData.id, chunkSize);
		const buffer = await this.helpers.binaryToBuffer(stream);
		fileBase64 = buffer.toString('base64');
	} else {
		fileBase64 = binaryData.data;
	}

	const bufferString = Buffer.from(fileBase64, BINARY_ENCODING);

	// Track and cleanup temp files at exit
	temp.track();

	const tempDbPath = temp.path({ suffix: '.sqlite' });
	fs.writeFileSync(tempDbPath, bufferString);

	// Initialize a new SQLite database from the temp file
	const tempDb = new sqlite3.Database(tempDbPath, (error: Error | null) => {
		if (error) {
			throw new NodeOperationError(this.getNode(), 'Could not connect to database');
		}
	});
	tempDb.close();

	return new DataSource({
		type: 'sqlite',
		database: tempDbPath,
	});
}
