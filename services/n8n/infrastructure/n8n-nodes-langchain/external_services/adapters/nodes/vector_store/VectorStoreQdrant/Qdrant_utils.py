"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vector_store/VectorStoreQdrant/Qdrant.utils.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vector_store/VectorStoreQdrant 的节点。导入/依赖:外部:@qdrant/js-client-rest；内部:n8n-workflow；本地:无。导出:QdrantCredential、createQdrantClient。关键函数/方法:parseQdrantUrl、createQdrantClient。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vector_store/VectorStoreQdrant/Qdrant.utils.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vector_store/VectorStoreQdrant/Qdrant_utils.py

import { QdrantClient } from '@qdrant/js-client-rest';
import { UserError } from 'n8n-workflow';

export type QdrantCredential = {
	qdrantUrl: string;
	apiKey: string;
};

function parseQdrantUrl(url: string): { protocol: string; host: string; port: number } {
	try {
		const parsedUrl = new URL(url);
		return {
			protocol: parsedUrl.protocol,
			host: parsedUrl.hostname,
			port: parsedUrl.port
				? parseInt(parsedUrl.port, 10)
				: parsedUrl.protocol === 'https:'
					? 443
					: 80,
		};
	} catch (error) {
		throw new UserError(
			`Invalid Qdrant URL: ${url}. Please provide a valid URL with protocol (http/https)`,
		);
	}
}

export function createQdrantClient(credentials: QdrantCredential): QdrantClient {
	const { protocol, host, port } = parseQdrantUrl(credentials.qdrantUrl);

	const qdrantClient = new QdrantClient({
		host,
		apiKey: credentials.apiKey,
		https: protocol === 'https:',
		port,
	});

	return qdrantClient;
}
