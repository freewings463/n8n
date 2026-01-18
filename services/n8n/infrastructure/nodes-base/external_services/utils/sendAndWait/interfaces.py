"""
MIGRATION-META:
  source_path: packages/nodes-base/utils/sendAndWait/interfaces.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/utils/sendAndWait 的工具。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:IEmail。关键函数/方法:无。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Integration package defaulted to infrastructure/external_services
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/utils/sendAndWait/interfaces.ts -> services/n8n/infrastructure/nodes-base/external_services/utils/sendAndWait/interfaces.py

import type { IDataObject } from 'n8n-workflow';

export interface IEmail {
	from?: string;
	to?: string;
	cc?: string;
	bcc?: string;
	replyTo?: string;
	inReplyTo?: string;
	reference?: string;
	references?: string;
	subject: string;
	body: string;
	htmlBody?: string;
	attachments?: IDataObject[];
}
