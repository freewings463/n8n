"""
MIGRATION-META:
  source_path: packages/core/nodes-testing/credential-types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/core/nodes-testing 的类型。导入/依赖:外部:无；内部:@n8n/di、n8n-workflow；本地:./load-nodes-and-credentials。导出:CredentialTypes。关键函数/方法:recognizes、getByName、getSupportedNodes、getParentTypes。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/nodes-testing/credential-types.ts -> services/n8n/infrastructure/core/external_services/adapters/credentials/nodes-testing/credential_types.py

import { Service } from '@n8n/di';
import type { ICredentialType, ICredentialTypes } from 'n8n-workflow';

import { LoadNodesAndCredentials } from './load-nodes-and-credentials';

@Service()
export class CredentialTypes implements ICredentialTypes {
	constructor(private readonly loadNodesAndCredentials: LoadNodesAndCredentials) {}

	recognizes(type: string): boolean {
		return this.loadNodesAndCredentials.recognizesCredential(type);
	}

	getByName(type: string): ICredentialType {
		return this.loadNodesAndCredentials.getCredential(type).type;
	}

	getSupportedNodes(type: string): string[] {
		return this.loadNodesAndCredentials.known.credentials[type]?.supportedNodes ?? [];
	}

	getParentTypes(_type: string): string[] {
		return [];
	}
}
