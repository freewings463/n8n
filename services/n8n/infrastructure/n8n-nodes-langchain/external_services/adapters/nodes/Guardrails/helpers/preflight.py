"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/Guardrails/helpers/preflight.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/Guardrails/helpers 的节点。导入/依赖:外部:无；内部:无；本地:../actions/types。导出:applyPreflightModifications。关键函数/方法:applyPreflightModifications、maskText。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/Guardrails/helpers/preflight.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/Guardrails/helpers/preflight.py

import type { GuardrailResult } from '../actions/types';

export function applyPreflightModifications(
	data: string,
	preflightResults: GuardrailResult[],
): string {
	if (preflightResults.length === 0) {
		return data;
	}

	// Get PII mappings from preflight results for individual text processing
	const piiMappings: Record<string, string> = {};
	for (const result of preflightResults) {
		if (result.info?.maskEntities) {
			const detected = result.info.maskEntities;
			for (const [entityType, entities] of Object.entries(detected)) {
				for (const entity of entities) {
					// Map original PII to masked token
					piiMappings[entity] = `<${entityType}>`;
				}
			}
		}
	}

	if (Object.keys(piiMappings).length === 0) {
		return data;
	}

	const maskText = (text: string): string => {
		if (typeof text !== 'string') {
			return text;
		}

		let maskedText = text;

		// Sort PII entities by length (longest first) to avoid partial replacements
		// This ensures longer matches are processed before shorter ones
		const sortedPii = Object.entries(piiMappings).sort((a, b) => b[0].length - a[0].length);

		for (const [originalPii, maskedToken] of sortedPii) {
			if (maskedText.includes(originalPii)) {
				// Use split/join instead of regex to avoid regex injection
				// This treats all characters literally and is safe from special characters
				maskedText = maskedText.split(originalPii).join(maskedToken);
			}
		}

		return maskedText;
	};
	return maskText(data);
}
