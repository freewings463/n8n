"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtop/actions/interaction/helpers.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtop/actions 的工具。导入/依赖:外部:无；内部:n8n-workflow；本地:../transport/types。导出:constructInteractionRequest。关键函数/方法:constructInteractionRequest。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtop/actions/interaction/helpers.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtop/actions/interaction/helpers.py

import type { IExecuteFunctions } from 'n8n-workflow';

import type { IAirtopInteractionRequest } from '../../transport/types';

export function constructInteractionRequest(
	this: IExecuteFunctions,
	index: number,
	parameters: Partial<IAirtopInteractionRequest> = {},
): IAirtopInteractionRequest {
	const additionalFields = this.getNodeParameter('additionalFields', index);
	const request: IAirtopInteractionRequest = {
		...parameters,
		configuration: {
			...(parameters.configuration ?? {}),
		},
	};

	if (additionalFields.visualScope) {
		request.configuration.visualAnalysis = {
			scope: additionalFields.visualScope as string,
		};
	}

	if (additionalFields.waitForNavigation) {
		request.waitForNavigation = true;
		request.configuration.waitForNavigationConfig = {
			waitUntil: additionalFields.waitForNavigation as string,
		};
	}

	return request;
}
