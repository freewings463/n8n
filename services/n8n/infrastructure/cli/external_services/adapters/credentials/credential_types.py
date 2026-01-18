"""
MIGRATION-META:
  source_path: packages/cli/src/credential-types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src 的类型。导入/依赖:外部:无；内部:@n8n/di、n8n-workflow、@/load-nodes-and-credentials；本地:无。导出:CredentialTypes。关键函数/方法:recognizes、getByName、getSupportedNodes、getParentTypes。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ICredentialType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/credential-types.ts -> services/n8n/infrastructure/cli/external_services/adapters/credentials/credential_types.py

import { Service } from '@n8n/di';
import type { ICredentialType, ICredentialTypes } from 'n8n-workflow';

import { LoadNodesAndCredentials } from '@/load-nodes-and-credentials';

@Service()
export class CredentialTypes implements ICredentialTypes {
	constructor(private loadNodesAndCredentials: LoadNodesAndCredentials) {}

	recognizes(type: string) {
		const { loadedCredentials, knownCredentials } = this.loadNodesAndCredentials;
		return type in knownCredentials || type in loadedCredentials;
	}

	getByName(credentialType: string): ICredentialType {
		return this.loadNodesAndCredentials.getCredential(credentialType).type;
	}

	getSupportedNodes(type: string): string[] {
		return this.loadNodesAndCredentials.knownCredentials[type]?.supportedNodes ?? [];
	}

	/**
	 * Returns all parent types of the given credential type
	 */
	getParentTypes(typeName: string): string[] {
		const extendsArr = this.loadNodesAndCredentials.knownCredentials[typeName]?.extends ?? [];

		if (extendsArr.length === 0) return [];

		const extendsArrCopy = [...extendsArr];

		for (const type of extendsArrCopy) {
			extendsArrCopy.push(...this.getParentTypes(type));
		}

		return extendsArrCopy;
	}
}
