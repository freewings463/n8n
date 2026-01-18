"""
MIGRATION-META:
  source_path: packages/nodes-base/credentials/common/http.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/credentials/common 的凭证。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:getUrl。关键函数/方法:getUrl。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Credentials definition -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/credentials/common/http.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/credentials/common/http.py

import type { IHttpRequestOptions, IRequestOptions } from 'n8n-workflow';

export const getUrl = (options: IHttpRequestOptions | IRequestOptions): string => {
	if (options.url) {
		return new URL(options.url, options.baseURL).toString();
	}
	if ('uri' in options && options.uri) {
		return options.uri;
	}
	throw new Error('No URL found in request options');
};
