"""
MIGRATION-META:
  source_path: packages/cli/src/modules/dynamic-credentials.ee/services/resolver-config-expression.service.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/dynamic-credentials.ee/services 的服务。导入/依赖:外部:无；内部:@n8n/decorators、@n8n/di、n8n-core、n8n-workflow、@/node-types、@/workflow-execute-additional-data；本地:无。导出:ResolverConfigExpressionService。关键函数/方法:resolve。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/dynamic-credentials.ee/services/resolver-config-expression.service.ts -> services/n8n/application/cli/services/resolver_config_expression_service.py

import { CredentialResolverConfiguration } from '@n8n/decorators';
import { Service } from '@n8n/di';
import { getNonWorkflowAdditionalKeys } from 'n8n-core';
import type { INode, INodeParameters } from 'n8n-workflow';
import { isNodeParameters, Workflow } from 'n8n-workflow';

import { NodeTypes } from '@/node-types';
import { getBase } from '@/workflow-execute-additional-data';

/**
 * Service for resolving expressions in credential resolver configurations.
 * Uses global data only (secrets, variables) without runtime execution context.
 */
@Service()
export class ResolverConfigExpressionService {
	constructor(private readonly nodeTypes: NodeTypes) {}

	/**
	 * Resolves expressions in config using global data only (secrets, variables).
	 * Does not use runtime execution context or workflow data.
	 * @throws Error if expression syntax is invalid
	 */
	async resolve(
		config: CredentialResolverConfiguration,
		canUseExternalSecrets = false,
	): Promise<CredentialResolverConfiguration> {
		// If config is not INodeParameters, return as is
		if (!isNodeParameters(config)) {
			return config;
		}

		// Create a minimal workflow with the mock node to leverage the expression resolver
		const workflow = new Workflow({
			nodes: [],
			connections: {},
			active: false,
			nodeTypes: this.nodeTypes,
		});

		const additionalData = await getBase();
		const additionalKeys = getNonWorkflowAdditionalKeys(additionalData, {
			secretsEnabled: canUseExternalSecrets,
		});

		return workflow.expression.getComplexParameterValue(
			// Use a mock node (mandatory) to resolve expressions in the config
			{
				id: '1',
				name: 'Mock Node',
			} as INode,
			config,
			'manual',
			additionalKeys,
			undefined,
			undefined,
			config,
		) as INodeParameters;
	}
}
