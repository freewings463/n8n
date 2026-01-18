"""
MIGRATION-META:
  source_path: packages/cli/src/services/naming.service.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/services 的服务。导入/依赖:外部:无；内部:@n8n/db、@n8n/di；本地:无。导出:NamingService。关键函数/方法:getUniqueWorkflowName、getUniqueCredentialName、getUniqueName。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/services/naming.service.ts -> services/n8n/application/cli/services/naming_service.py

import { CredentialsRepository, WorkflowRepository } from '@n8n/db';
import { Service } from '@n8n/di';

@Service()
export class NamingService {
	constructor(
		private readonly workflowRepository: WorkflowRepository,
		private readonly credentialsRepository: CredentialsRepository,
	) {}

	async getUniqueWorkflowName(requestedName: string) {
		return await this.getUniqueName(requestedName, 'workflow');
	}

	async getUniqueCredentialName(requestedName: string) {
		return await this.getUniqueName(requestedName, 'credential');
	}

	private async getUniqueName(requestedName: string, entity: 'workflow' | 'credential') {
		const repository = entity === 'workflow' ? this.workflowRepository : this.credentialsRepository;

		const found = await repository.findStartingWith(requestedName);

		if (found.length === 0) return requestedName;

		if (found.length === 1) return [requestedName, 2].join(' ');

		const maxSuffix = found.reduce((max, { name }) => {
			const [_, strSuffix] = name.split(`${requestedName} `);

			const numSuffix = parseInt(strSuffix);

			if (isNaN(numSuffix)) return max;

			if (numSuffix > max) max = numSuffix;

			return max;
		}, 2);

		return [requestedName, maxSuffix + 1].join(' ');
	}
}
