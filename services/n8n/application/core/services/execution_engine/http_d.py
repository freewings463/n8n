"""
MIGRATION-META:
  source_path: packages/core/src/http.d.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src 的类型。导入/依赖:外部:http-proxy-agent、https-proxy-agent；内部:无；本地:无。导出:无。关键函数/方法:addRequest。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Core src/* defaulted to execution engine application services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/http.d.ts -> services/n8n/application/core/services/execution_engine/http_d.py

import type http from 'http-proxy-agent';
import type https from 'https-proxy-agent';

declare module 'http' {
	interface Agent {
		addRequest(req: ClientRequest, options: http.HttpProxyAgentOptions): void;
	}
}

declare module 'https' {
	interface Agent {
		addRequest(req: ClientRequest, options: https.HttpsProxyAgentOptions): void;
	}
}
